#!/usr/bin/env bash
#
# Open the student download the way a student opens it, in a VS Code that has
# never seen it before.
#
# This exists because the obvious way to test "does the kernel get picked up"
# does not work. VS Code remembers the kernel you chose *per folder path*, and
# your extensions, settings and environment history live in your user profile.
# So the second time you test a folder it cannot fail, and it cannot fail on
# your machine at all once you have selected the kernel there once. Every
# ingredient of the test has to be new: a folder path that has never been
# opened, and a VS Code profile that has never been used.
#
# What it does:
#
#   1. builds the download from this repository
#   2. unzips it to a fresh temporary path
#   3. runs `pixi install` in it, like a student would
#   4. checks the environment exposes a kernel at all (scripts/check_env_kernel.py)
#   5. opens it in a VS Code with a throwaway user-data-dir and extensions-dir
#
# By default step 5 starts with no extensions installed, so you see what a
# student sees. Pass --with-extensions to install them first and go straight to
# the kernel question.
#
# Two things will look broken and are not. VS Code opens every new folder in
# Restricted Mode without asking (the default of
# security.workspace.trust.startupPrompt changed from "once" to "never" in
# 1.126), and while a folder is untrusted its extensions do not run, so the
# "install the recommended extensions" notification usually never appears
# either. Both are what a student gets. The checklist below is the order that
# works, and it is the same order the Getting Started chapter gives.
#
# Usage:
#
#     scripts/vscode_kernel_smoketest.sh
#     scripts/vscode_kernel_smoketest.sh --with-extensions
#     scripts/vscode_kernel_smoketest.sh --no-vscode     # steps 1-4 only
#
# It deliberately does not clean up after itself: the folder it made is the
# evidence. It prints the path and the command to remove it.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WITH_EXTENSIONS=0
LAUNCH_VSCODE=1

for arg in "$@"; do
    case "$arg" in
        --with-extensions) WITH_EXTENSIONS=1 ;;
        --no-vscode)       LAUNCH_VSCODE=0 ;;
        -h|--help)         awk 'NR>1 && /^#/ {sub(/^# ?/, ""); print; next} NR>1 {exit}' \
                               "${BASH_SOURCE[0]}"; exit 0 ;;
        *)                 echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

command -v pixi >/dev/null || { echo "error: pixi is not on PATH" >&2; exit 1; }

# A fresh path every run. This is the part that makes the test mean anything:
# VS Code keys its remembered kernel on the folder path, so reusing a path
# tests nothing.
SANDBOX="$(mktemp -d "${TMPDIR:-/tmp}/im-smoketest.XXXXXXXX")"
echo "sandbox: $SANDBOX"
echo

echo "==> 1/5  building the download"
python3 "$REPO/scripts/build_student_folder.py" --out "$SANDBOX/site" >/dev/null
echo "    $(du -h "$SANDBOX/site/instructing-machines.zip" | cut -f1) zip"

echo "==> 2/5  unzipping it, the way a student does"
unzip -q "$SANDBOX/site/instructing-machines.zip" -d "$SANDBOX"
FOLDER="$SANDBOX/instructing-machines"
test -f "$FOLDER/.vscode/settings.json" || { echo "    FAILED: no .vscode in the zip" >&2; exit 1; }
test -f "$FOLDER/week1/notebooks.ipynb" || { echo "    FAILED: no week1 notebook in the zip" >&2; exit 1; }
echo "    $FOLDER"

echo "==> 3/5  pixi install (this is the slow one)"
pixi install --manifest-path "$FOLDER/pixi.toml"

echo "==> 4/5  doing what pixi run check does, and checking it took"
# `pixi run check` is what a student runs. It depends on both of these tasks:
# `kernel` registers the course kernelspec, and `vscode` writes the path to
# pixi into .vscode/settings.json so the pixi extension can find it however
# VS Code was started. Calling them directly does the same work without the
# pages of environment diagnostics that `im check` prints.
pixi run --manifest-path "$FOLDER/pixi.toml" kernel 2>&1 | sed 's/^/    /'
pixi run --manifest-path "$FOLDER/pixi.toml" vscode 2>&1 | sed 's/^/    /'
pixi run --manifest-path "$FOLDER/pixi.toml" \
    python "$REPO/scripts/check_env_kernel.py" | sed 's/^/    /'

if [ "$LAUNCH_VSCODE" -eq 0 ]; then
    echo
    echo "Stopping before VS Code, as asked."
    echo "Remove the sandbox with:  rm -rf $SANDBOX"
    exit 0
fi

command -v code >/dev/null || {
    echo
    echo "error: the 'code' command is not on PATH, so VS Code cannot be started" >&2
    echo "       On a Mac: run 'Shell Command: Install code command in PATH' from" >&2
    echo "       the command palette in VS Code, then run this again." >&2
    echo "       The folder is ready at: $FOLDER" >&2
    exit 1
}

USER_DATA="$SANDBOX/vscode-user"
EXTENSIONS="$SANDBOX/vscode-extensions"
mkdir -p "$USER_DATA" "$EXTENSIONS"

if [ "$WITH_EXTENSIONS" -eq 1 ]; then
    echo "==> 5/5  installing the extensions into the throwaway profile"
    # Same list as student-folder/vscode/extensions.json. pixi-code
    # pulls in ms-python.vscode-python-envs on its own, so installing it here
    # is belt and braces.
    for extension in ms-python.python ms-toolsai.jupyter quarto.quarto renan-r-santos.pixi-code; do
        code --user-data-dir "$USER_DATA" --extensions-dir "$EXTENSIONS" \
             --install-extension "$extension" --force 2>&1 | sed 's/^/    /'
    done
else
    echo "==> 5/5  opening with no extensions, so you see the prompt a student sees"
fi

echo
echo "Opening VS Code. Do exactly what the chapter tells a student to do:"
echo
echo "  1. TRUST. Bottom left, click the blue 'Restricted Mode' button, then"
echo "     'Trust', then close the panel. Nothing asked you to. That is the"
echo "     current VS Code default, not a fault of this test, and until you do"
echo "     it every extension in this window is switched off."
if [ "$WITH_EXTENSIONS" -eq 0 ]; then
    echo "  2. INSTALL. Extensions panel on the left, search '@recommended',"
    echo "     install all four (Python, Jupyter, Quarto, Pixi). A notification"
    echo "     may offer to do it for you. It usually does not. Do not wait."
else
    echo "  2. INSTALL. Already done — the four are in this throwaway profile."
fi
echo "  3. RELOAD. Cmd/Ctrl+Shift+P, 'Developer: Reload Window'."
echo
echo "     A warning that the default environment manager 'is not registered'"
echo "     is expected: python-envs reads that setting before pixi-code has"
echo "     registered. It registers a moment later. Removing the setting"
echo "     silences the warning and costs the kernel its name."
echo
echo "Then the things being tested:"
echo "  4. open week1/notebooks.ipynb"
echo "  5. top right: Select Kernel -> Jupyter Kernel. There should be exactly"
echo "     one entry, ours, with .pixi in its path. VS Code labels a kernel"
echo "     from the environment it lives in, not from our kernelspec, and it"
echo "     cannot name a pixi environment -- so expect a path, not a name."
echo "  6. run the first cell: does a widget render? And is a callout in a"
echo "     markdown cell a coloured box rather than raw text with colons?"
echo
echo "Remove the sandbox when you are done:  rm -rf $SANDBOX"
echo

code --user-data-dir "$USER_DATA" --extensions-dir "$EXTENSIONS" \
     --new-window "$FOLDER"
