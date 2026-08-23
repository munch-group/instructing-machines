#!/usr/bin/env python3
"""Check that the installed course environment exposes a usable notebook kernel.

Run it *inside* the student environment, which is where it can see what a
student's VS Code will see::

    pixi run --manifest-path student-folder/pixi.toml python scripts/check_env_kernel.py

The course registers no kernel of its own — ``pixi.toml`` promises that nothing
is installed outside the course folder, and a named kernelspec would have to go
in the user's Jupyter directory to be found. So the only kernel a student has is
the one ipykernel writes into the environment prefix when pixi installs it, at
``.pixi/envs/default/share/jupyter/kernels/python3``. Everything downstream
depends on that file existing and pointing somewhere real: VS Code offers it,
`pixi run clean-notebooks` executes through it, and every widget in the book
runs on it.

Three things can go wrong, and all three have:

- ipykernel installs but writes no kernelspec, which is a per-platform failure
  and the reason this runs on all four in CI rather than on the machine that
  happened to build the zip.
- The kernelspec resolves to a Python outside the environment, which means a
  student would be running the book on some other interpreter with none of the
  widgets.
- The folder was moved after ``pixi install``. A pixi environment is not
  relocatable: the kernelspec stores an absolute path, so moving the folder
  leaves a kernel that VS Code still lists and that dies the moment it starts.

Exit status is 0 when the kernel is present, inside this environment, and
runnable, and 1 with an explanation otherwise.
"""

from __future__ import annotations

import subprocess
import sys
import sysconfig
from pathlib import Path

# The name ipykernel gives its own kernelspec. The book's notebooks name this
# in their metadata too (see scripts/check_notebook_kernels.py), so the two
# have to agree.
KERNEL_NAME = "python3"


def fail(message: str, *details: str) -> int:
    print(f"FAILED: {message}", file=sys.stderr)
    for line in details:
        print(f"        {line}", file=sys.stderr)
    return 1


def main() -> int:
    prefix = Path(sys.prefix).resolve()
    print(f"environment: {prefix}")
    print(f"python:      {sys.version.split()[0]}")

    try:
        from jupyter_client.kernelspec import KernelSpecManager
    except ImportError as error:
        return fail("jupyter_client is not importable in this environment", str(error))

    specs = KernelSpecManager().get_all_specs()
    if KERNEL_NAME not in specs:
        return fail(
            f"the environment exposes no kernelspec named {KERNEL_NAME!r}",
            f"it has: {', '.join(sorted(specs)) or '(nothing)'}",
            "ipykernel should have written one into",
            f"{prefix / 'share' / 'jupyter' / 'kernels' / KERNEL_NAME}",
        )

    spec = specs[KERNEL_NAME]["spec"]
    resource_dir = Path(specs[KERNEL_NAME]["resource_dir"]).resolve()
    interpreter = Path(spec["argv"][0])
    print(f"kernelspec:  {resource_dir}")
    print(f"argv[0]:     {interpreter}")

    # A kernelspec found through some *other* interpreter's data directory is
    # not this environment's, and would start the book on the wrong Python.
    if not resource_dir.is_relative_to(prefix):
        return fail(
            "the kernelspec found is not this environment's",
            f"it lives in {resource_dir}, outside {prefix}",
            "a student would be running the notebooks on a different Python,",
            "with none of the course widgets installed",
        )

    # The symptom of a folder moved after `pixi install`: VS Code still lists
    # the kernel, and it dies on start.
    if not interpreter.exists():
        return fail(
            "the kernelspec points at an interpreter that does not exist",
            f"{interpreter}",
            "a pixi environment is not relocatable — if this folder was moved",
            "or renamed after `pixi install`, run `pixi install` again",
        )

    # Same trap, one step subtler: the path exists but belongs to a different
    # environment that happens to sit where this one used to.
    if not interpreter.resolve().is_relative_to(prefix):
        return fail(
            "the kernelspec points outside this environment",
            f"{interpreter.resolve()} is not under {prefix}",
        )

    # Everything above is a file on disk saying the kernel should work. This is
    # the only step that finds out whether it does.
    probe = subprocess.run(
        [str(interpreter), "-c",
         "import ipykernel_launcher, ipywidgets, anywidget; print('ok')"],
        capture_output=True, text=True, timeout=120,
    )
    if probe.returncode != 0:
        return fail(
            "the kernel's interpreter cannot start a kernel",
            *(probe.stderr.strip().splitlines()[-6:] or ["(no output)"]),
        )

    print(f"platform:    {sysconfig.get_platform()}")
    print(f"\nOK: {KERNEL_NAME!r} is registered in this environment and starts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
