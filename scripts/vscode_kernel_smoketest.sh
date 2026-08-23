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
# By default step 5 starts with no extensions installed, so you also see what a
# student sees: the "install the recommended extensions" prompt. Pass
# --with-extensions to install them first and go straight to the kernel
# question.
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
        -h|--help)         sed -n '2,36p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
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

echo "==> 4/5  is there a kernel to find?"
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
    for extension in ms-python.python ms-toolsai.jupyter renan-r-santos.pixi-code; do
        code --user-data-dir "$USER_DATA" --extensions-dir "$EXTENSIONS" \
             --install-extension "$extension" --force 2>&1 | sed 's/^/    /'
    done
else
    echo "==> 5/5  opening with no extensions, so you see the prompt a student sees"
fi

echo
echo "Opening VS Code. What to look for, in order:"
if [ "$WITH_EXTENSIONS" -eq 0 ]; then
    echo "  1. a notification offering the recommended extensions. It should"
    echo "     name Python, Jupyter and Pixi. Accept it and let it finish."
fi
echo "  2. open week1/notebooks.ipynb"
echo "  3. look at the top right. Does it already name a kernel with .pixi in"
echo "     its path, or does it say 'Select Kernel'?"
echo "  4. if you have to pick one, is the .pixi entry in the list at all, and"
echo "     is it offered as the recommended one?"
echo "  5. run the first cell and check a widget renders."
echo
echo "Remove the sandbox when you are done:  rm -rf $SANDBOX"
echo

code --user-data-dir "$USER_DATA" --extensions-dir "$EXTENSIONS" \
     --new-window "$FOLDER"
