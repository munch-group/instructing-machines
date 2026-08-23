#!/usr/bin/env python3
"""Execute every notebook the book renders, then strip its outputs.

The book ships with ``execute: enabled: false`` in ``docs/_quarto.yml``, so
Quarto never runs a notebook at render time — it just displays whatever code
is in the source file, with no output. That's deliberate: a student who
downloads a chapter should get the same notebook the website shows, and
neither should already contain the answer to a "predict, then run" exercise.

Correctness is therefore not Quarto's job. This script is: it executes each
notebook for real (via nbconvert, in the project's own kernel, so a broken
cell fails loudly here rather than shipping silently), then clears every
cell's output and execution count, and finally strips the two things plain
``nbconvert --clear-output`` leaves behind — the notebook-level
``metadata.widgets`` blob and each code cell's ``metadata.execution``
timestamps — so a clean run produces a clean diff.

It also normalizes each notebook's kernel metadata on the way past, via
``scripts/check_notebook_kernels.py``. nbconvert stamps the executing machine's
kernel name and Python version into every notebook it runs, and that stamp is
what VS Code reads when it decides which kernel a freshly downloaded notebook
wants. Left alone it names an environment only this machine has. Normalizing
here means the stamp is undone by the same command that applies it, rather than
by whoever notices.

The file list is read from the book's own config (the same chapters
``scripts/check-badge-order.py`` walks), not a hardcoded list or a blind glob,
so a notebook added to or dropped from the book is picked up automatically
and a notebook that isn't part of the book (a demo, a draft) is left alone.

One exception: KEEP_OUTPUT below. python/course-tools.ipynb exists to show
what each widget actually looks like when it runs; with Quarto never
executing at render time, that page only has anything to show if its output
is baked into the file. It's still executed on every run — a broken demo
cell still fails the build — just not stripped afterward.

Run it with no arguments from anywhere in the repository::

    pixi run clean-notebooks

Exit status is 0 when every notebook executes cleanly, 1 if any one of them
raises, so it can sit in the render/CI workflow as a quality gate.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import nbformat

# quarto_profile lives next to this script, so import it by the script's own
# location rather than trusting the working directory: build_student_folder.py
# runs from docs/ as Quarto's post-render hook, and todo.py loads
# check-badge-order.py by path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from quarto_profile import quarto_config  # noqa: E402
from check_notebook_kernels import normalize as normalize_kernel  # noqa: E402

CHAPTER = re.compile(r"^\s*-\s+(?!part:)([\w./-]+\.ipynb)\s*$")

# The kernelspec ipykernel installs into any environment it is part of.
# Distinct from the course kernel the notebooks name — see the comment in
# execute_and_clean, and scripts/check_notebook_kernels.py.
BASE_KERNEL = "python3"

DEFAULT_WORKERS = 4
EXECUTE_TIMEOUT = 180  # seconds per cell; sandbox_widget spawns a subprocess per cell

# Chapters whose baked-in output survives the strip — see the module
# docstring. Paths are relative to docs/, matching how they appear in
# the book's config.
KEEP_OUTPUT = {"python/course-tools.ipynb"}


def chapters_in_order(quarto_yml: Path):
    """Yield every .ipynb chapter path the book actually renders, in order."""
    for line in quarto_yml.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("#"):
            continue
        match = CHAPTER.match(line)
        if match:
            yield match.group(1)


def clean_metadata(nb) -> None:
    """Strip what ``nbconvert --clear-output`` leaves behind on its own."""
    nb.metadata.pop("widgets", None)
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        cell.execution_count = None
        cell.outputs = []
        cell.metadata.pop("execution", None)


def execute_and_clean(path: Path, docs: Path) -> tuple[Path, bool, str]:
    """Execute ``path`` in place, then clear its output unless it's in
    KEEP_OUTPUT. Returns (path, ok, message)."""
    result = subprocess.run(
        [
            "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace",
            f"--ExecutePreprocessor.timeout={EXECUTE_TIMEOUT}",
            # Execute on the kernelspec ipykernel writes into every
            # environment, not the one named in the notebook. The notebooks
            # name the course kernel so that VS Code suggests it to a
            # student, and that kernel is registered by `pixi run check` on
            # a student's machine — which CI never runs, having only
            # installed the environment. Pinning it here keeps executing a
            # notebook independent of what its metadata asks for.
            f"--ExecutePreprocessor.kernel_name={BASE_KERNEL}",
            str(path),
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        # Leave the notebook exactly as it failed — outputs included — so the
        # error is visible to whoever opens it next, rather than silently
        # discarding the evidence.
        tail = "\n".join(result.stderr.strip().splitlines()[-15:])
        return path, False, tail

    # Read back what nbconvert wrote and undo its two stamps: the kernel
    # metadata always, the outputs unless this is a notebook whose baked-in
    # output is the whole point of the page.
    nb = nbformat.read(path, as_version=4)
    normalize_kernel(nb)
    if path.relative_to(docs).as_posix() not in KEEP_OUTPUT:
        clean_metadata(nb)
    nbformat.write(nb, path)
    return path, True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                        help=f"notebooks to execute concurrently (default {DEFAULT_WORKERS})")
    args = parser.parse_args()

    docs = Path(__file__).resolve().parent.parent / "docs"
    quarto_yml = quarto_config(docs)
    if not quarto_yml.exists():
        print(f"cannot find {quarto_yml}", file=sys.stderr)
        return 1

    paths = [docs / chapter for chapter in chapters_in_order(quarto_yml)]
    missing = [p for p in paths if not p.exists()]
    for p in missing:
        print(f"WARNING: {p} is listed in {quarto_yml.name} but not on disk — skipping",
              file=sys.stderr)
    paths = [p for p in paths if p.exists()]

    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(execute_and_clean, p, docs): p for p in paths}
        for future in as_completed(futures):
            path, ok, message = future.result()
            rel = path.relative_to(docs)
            if ok:
                note = " (output kept)" if rel.as_posix() in KEEP_OUTPUT else ""
                print(f"clean: {rel}{note}")
            else:
                print(f"FAILED: {rel}", file=sys.stderr)
                failures.append((rel, message))

    if failures:
        print(f"\n{len(failures)} notebook(s) failed to execute cleanly:", file=sys.stderr)
        for rel, message in failures:
            print(f"\n=== {rel} ===\n{message}", file=sys.stderr)
        return 1

    print(f"\n{len(paths)} notebook(s) executed and cleaned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
