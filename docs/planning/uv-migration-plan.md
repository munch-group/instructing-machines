# Plan: moving the student environment from pixi to uv

Status: revision 5, 2026-10-10. Nothing has been built yet.

This revision went through two rounds of five adversarial reviews. The first
round covered uv/VS Code facts, the im-course-tools code, the student's first
day, rollout/CI and the book repo. The second round, on the simplified
revision 4, covered VS Code behavior checked against the extensions' source,
uv claims tested with uv 0.13.0, a walk-through of the student steps,
internal consistency, and diagnosability. Kasper's decisions are recorded
where they apply and listed in "Decisions log" at the end. Marks used: "tested"
means checked locally with uv 0.13.0; "source" means read in the current
vscode-python-environments (v1.41.0), vscode-python, vscode-jupyter or vscode
source; "docs" means checked against current documentation only.

## Goal

Replace pixi with uv as the tool that builds the student course environment,
and drop the `munch-group.im-pixi-vscode` extension. VS Code's Python and
Jupyter extensions understand a workspace `.venv` natively, so the
kernel-discovery problems of the pixi setup go away, and students can follow
VS Code's own prompts without breaking the course setup.

## Decisions

1. **Next cohort only.** No migration bridge for students currently on pixi.
   Everything published today keeps working, unchanged, until the swap.
2. **Pixi cleanup is an explicit command, `im retire-pixi`**, not part of
   `im update`. `~/.pixi` is never touched, except for removing the course's own
   `pixi global` copy of `im-course-tools` (BSF uses pixi).
3. **Kernel:** VS Code's own `.venv` kernel and no named kernelspec. The kernel
   checks are inverted (a kernelspec must be absent) rather than deleted,
   because VS Code writes one back into a notebook on every save.
4. **settings.json:** Kasper's version plus `jupyter.widgetScriptSources: []`,
   `jupyter.notebookFileRoot: "${workspaceFolder}"`,
   `notebook.output.textLineLimit: 60`, and the `python-envs.pythonProjects`
   entry that makes `.venv` the folder's interpreter (see "Making `.venv` the
   default interpreter"). Nothing that only repeats a default.
5. **Root `pixi.toml` stays** as the author's environment.
6. **No Quarto CLI** in the student environment, provided a test first shows
   the Quarto extension still renders callouts in notebook markdown without it.
   If it does not, the options (Quarto's installer, or PyPI `quarto-cli` with
   hard testing) come back to Kasper.
7. **After setup, students work only in VS Code's terminal**, where `im`,
   `python` and `uv` are all available.
8. **No `im setup`; `widget-check.ipynb` is the day-one acceptance test, and
   `im doctor` is the troubleshooter**, with a no-Python fallback script for the
   cases where `im doctor` cannot run (see "Diagnosing failures").
9. **uv-managed Python only**, with a documented override for TAs.
10. **`.pin_shell_path.*` kept**, ported to uv, run by nothing, but kept
    current by `im update` so they can be switched on later.

## Release safety

Every `im get`, `im update` and `im doctor` calls `upgrade_if_newer`
(`cli.py:130,149,231`). It asks the index the running `im` came from for the
latest version (`release.py:311`) and upgrades without asking. For a pixi
student that index is the munch-group conda channel, and the upgrade is
`pixi update im-course-tools`. The folder caps the package at `<0.2`, so the
upgrade changes nothing, `upgrade()` exits 1 (`release.py:615-622`), and the
command the student typed never runs. That happens on every invocation, from
the moment 0.2.0 or any `v0.2.0.rc*` tag reaches the channel. Verified in the
source. Therefore:

- **0.2.x is published to PyPI only** until every pixi-era folder is retired.
  `conda-release.yml` gets a guard that skips `v0.2*` tags, merged before the
  first 0.2 tag exists.
- **No 0.2 rc tags** until that guard is in place.

## Published paths, before and after the swap

Old `im update` requires `pixi.toml`/`pixi.lock` inside the published zip
(`environment.py:138,145`), and old `im get` fetches project zips from fixed
URLs. Retakers, re-exam students and TAs on pixi folders would lose both on
swap day if those files moved.

- **The uv world gets new paths:** `uv/instructing-machines.zip`,
  `uv/pyproject.toml`, `uv/uv.lock`, `uv/projects/*.zip`. im-course-tools 0.2
  reads only these. Its `ARCHIVE` (`environment.py:99`) and `url_for` /
  `DEFAULT_BASE_URL` (`course.py:14`) are repointed. The chapter's download
  command uses the `uv/` URL.
- **The pixi artifacts stay at their current paths, frozen.** The last pixi
  build goes up as a GitHub release, `pixi-final`, in the book repo. Every
  publish run downloads its assets and copies them into `_book` at the old
  paths, so the next Pages deploy cannot wipe them.
- **"End of term" means after the last re-exam.** The frozen paths are
  removed a term after that.
- **Rollback.** Reverting the merge restores the book. A PyPI release cannot
  be withdrawn and reused, so a broken 0.2.x is fixed forward with 0.2.(x+1).

## Branch strategy

- Develop in a separate worktree, on a `uv` branch in both repos. The
  pre-commit hook is selected by a relative `core.hooksPath`, so committing
  chapter edits from the `uv` checkout would run the branch's hook.
- **Keep the long-lived branch to new or additive things:** the uv folder,
  the new workflow, im-course-tools 0.2, and flags on shared scripts. Chapter
  wording and the kernelspec strip touch files Kasper edits weekly. They are
  done on swap day as **one scripted commit** (a script committed on the
  branch and run at merge), not carried as a diff for months. Rebase weekly.
- Shared scripts (`check_notebook_kernels.py`, `clean_notebooks.py`,
  `scripts/hooks/pre-commit`) get a mode flag, `--kernelspec named|absent`,
  defaulting to `named`, so nothing changes on main until the swap flips it.
- **im-course-tools during testing.** CI may use a git source
  (`[tool.uv.sources] im-course-tools = { git = ..., branch = "uv" }`).
  `uv.lock` pins the commit, so CI runs `uv lock --upgrade-package
  im-course-tools` before testing. Fresh-machine hand tests cannot use a git
  source (fresh Windows has no git; on a Mac it triggers the Xcode CLT dialog),
  so they use a TestPyPI pre-release or a wheel URL. After tagging 0.2.0:
  drop the sources block, run `uv lock --refresh-package im-course-tools`, and
  confirm CI is green.

## Student setup steps

This is what `getting_set_up.qmd` will give, in panel tabs per platform. Each
step states what success looks like, and to stop if it does not.

**1. Quit everything.** Quit VS Code completely (Cmd-Q on Mac, close every
window on Windows), Terminal or PowerShell, and Finder or Explorer windows on the
course folder.

**2. Download the course folder** in a new Terminal/PowerShell:
- Mac: `curl -fL -o ~/Downloads/instructing-machines.zip https://munch-group.org/instructing-machines/uv/instructing-machines.zip`
- Windows: `iwr -Uri "https://munch-group.org/instructing-machines/uv/instructing-machines.zip" -OutFile "$env:USERPROFILE\Downloads\instructing-machines.zip"`

`-f` makes curl fail on a 404 or a captive portal instead of saving the HTML
page as a "zip".

**3. Unpack it** to the fixed short path. The one-liner checks the zip before
anything is moved, so a bad download never leaves the student with no folder:
- Mac (bash one-liner): `unzip -tq` the zip, then move an existing
  `~/instructing-machines` aside to `-old-<timestamp>`, then unzip into `$HOME`.
- Windows: test the archive, `Move-Item ... -ErrorAction Stop` (it fails
  loudly if VS Code still holds the folder, instead of `Expand-Archive`
  printing a screen of red), then `Expand-Archive` to `C:\`.

Never "Extract All" into Downloads, and never into OneDrive.

**4. Install uv**, with the official one-liners:
- Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

**5. Build the course environment**, in the same window, calling uv by its full
path. The installer cannot change the PATH of the shell that ran it.
- Mac: `~/.local/bin/uv sync --directory ~/instructing-machines`
- Windows: `& "$HOME\.local\bin\uv.exe" sync --directory C:\instructing-machines`

Success means the last line reads `Installed N packages` and there is no red
text. **If you see red text, stop here.** A short table maps uv's own errors
to fixes:

| uv says | Fix |
|---|---|
| a certificate / `UnknownIssuer` error | antivirus (BitDefender, Avast, AVG, ESET, Kaspersky) is intercepting HTTPS: allow uv, or run the diagnose script |
| `No space left on device` | free disk space |
| `Access is denied` | antivirus or Smart App Control: run the diagnose script |
| "failed to hardlink, falling back to copy" (yellow) | harmless, ignore |

If step 5 says the file is not found (uv was installed somewhere unusual),
open a new Terminal/PowerShell and run `uv sync --directory ...` without the
path.

**5b. Only if you took the course before (you have a pixi-era folder):**
`uvx --from im-course-tools@latest im retire-pixi`. With no argument it finds
old course folders itself (`~/instructing-machines-old-*` and
`C:\instructing-machines-old-*`) and lists what it will remove before asking.
Then copy your own notebooks and week folders from the `-old-` folder across in
Finder/Explorer. Do not open the old folder in VS Code.

**6. VS Code.**
- Install it if needed. On a Mac, drag Visual Studio Code into Applications
  and open it from there. Run from Downloads it does not auto-update, and `im`
  cannot find it.
- Choose "Continue without signing in", and close every Welcome/Get Started
  tab.
- File → Open Folder → `instructing-machines`. Trust it, and do **not** tick
  "trust all files in the parent folder".
- Install the recommended extensions: from the toast, or, if it has vanished
  into the bell, from the Extensions panel, searching `@recommended`
  (screenshot). Close the Get Started walkthroughs those extensions open, and
  never click "Create Environment" or "Select Interpreter" there.
- If macOS offers to install developer tools, click Cancel.

**7. Open `widget-check.ipynb` and Run All.** On this first notebook VS Code
asks for a kernel twice: "Python Environments…", then the starred `.venv`
(two screenshots). Later notebooks remember it. The notebook prints a
diagnostic block, then shows each widget under a line saying what should
appear, and ends with a checklist (see "widget-check.ipynb"). To change a
wrongly picked kernel, click the kernel name at the top right.

**8. Terminal → New Terminal, and run `im doctor`.** This proves that the
terminal is activated (`im` found), that the Windows execution policy allows
it, and that the open folder is the course folder. It should end with no
failures.

From here on, the student uses only VS Code's terminal. The exceptions are
`im retire-pixi` and, on Windows, `im update` when files are locked: both may
ask to close VS Code and continue in a plain terminal, and the chapter says so.

### Why the steps are in this order

- **The environment is built before VS Code first opens the folder** (steps 5
  and 6). The Python Environments extension's priority chain
  (`interpreterSelection.ts`, `resolvePriorityChainCore`, source) ends in
  auto-discovery, which prefers `<project>/.venv` (`venvManager.ts`
  `loadEnvMap`, source). With `.venv` already present there is no
  "Create environment" offer. That trigger is off by default and skipped when
  `.venv/pyvenv.cfg` exists (`createEnvironmentTrigger.ts`, source). There is
  also no reload step. The shipped `pythonProjects` entry (see the next
  section) puts `.venv` above the two user-level settings that would otherwise
  beat the auto-pick: `python-envs.defaultEnvManager` and
  `python.defaultInterpreterPath`. A third setting,
  `python.useEnvironmentsExtension: false` (which im-pixi-vscode may have
  written), switches the extension off entirely. `im doctor` and
  `im retire-pixi` handle it.
- **The full uv path means no terminal restart.** `--directory` works from any
  folder and honors that folder's `[tool.uv]` (tested). The pixi chapter spent
  two steps on the restart.
- **The Windows execution policy needs no step of its own.** Since
  vscode-python-environments 1.30, terminal activation on Windows runs
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` itself
  before `Activate.ps1` (`managers/common/utils.ts`, source). `uv`, `uvx` and
  `im` are `.exe` files and not subject to the policy. Group Policy still
  overrides everything; `im doctor` reports that case and its advice. The
  workspace terminal profile from revision 3 and the PowerShell-profile guard
  are therefore dropped.
- **Activation needs the extension awake.** The Python Environments extension
  activates on `onLanguage:python`. A terminal opened before any `.py` or
  `.ipynb` has been opened stays inactive until one is (source). Step 7
  (a notebook) comes before step 8 (the terminal) for this reason, and the
  `hello-world` chapter opens `hello.py` before using the terminal.
- **Kernel selection is two clicks, not zero.** VS Code core auto-picks a
  kernel only when exactly one is Preferred. Jupyter marks one Preferred only
  after a pick from a kernel source, and before that just stars `.venv` as
  Recommended in the picker (`notebookKernelServiceImpl.ts`,
  `kernelSourceCommandHandler.ts`, `preferredKernelConnectionService.node.ts`,
  source).
- **The shell PATH needs no pin script.** On a Mac the uv installer writes its
  PATH line into `.profile`, `.bashrc`, `.bash_profile`, `.bash_login`,
  `.zshrc`, `.zshenv` and fish's `conf.d` (installer source). That covers
  both zsh and bash whichever is the default.

### Considered and rejected

- *`uv tool install im-course-tools` for a global `im`.* Students still need
  activation for `python hello.py`, and it would put a second `im` on the
  machine, outside the lock.
- *Letting VS Code create the environment.* It installs with `uv pip`, not
  from `uv.lock`.
- *Command Prompt as the Windows terminal.* It means a different command
  syntax from everything else.
- *A cross-platform `im install` that replaces steps 2-5 (S9).* Deferred:
  only if the one-liners keep causing trouble.
- *Converting a pixi-era folder in place.* Step 3 always gives a fresh uv
  folder, so a conversion step would only build a second `.venv` inside an
  archived folder. `im retire-pixi` cleans up and does not convert.

## Making `.venv` the default interpreter

Building `.venv` before VS Code first opens the folder should make the
auto-pick happen with no prompt. Even so, a student must not depend on seeing
and accepting a popup, or on nothing else having been chosen first. The
Python extension's "We noticed a new environment has been created. Do you want
to select it for the workspace folder?" appears when `.venv` is created after
the folder is already open, and it is easy to miss. So `.venv` is made the
default three ways.

**1. A workspace setting at the top of the selection chain.** The folder's
`.vscode/settings.json` carries:

```json
"python-envs.pythonProjects": [
    { "path": ".", "envManager": "ms-python.python:venv" }
]
```

The Python Environments extension resolves a folder's interpreter by priority
(`interpreterSelection.ts`, `resolvePriorityChainCore`, source):

1. a `pythonProjects` entry for the folder;
2. a configured `python-envs.defaultEnvManager`;
3. a configured `python.defaultInterpreterPath`;
4. auto-discovery.

The `pythonProjects` entry is priority 1. The relative `path` is resolved
against the workspace folder (`getProjectSpecificEnvManager`, source), and it
names the venv manager. That manager's `get` returns the project's `.venv`
(`venvManager.ts`, source). Nothing in the setting is machine- or
OS-specific, so it can be shipped in the zip.

It does three things auto-discovery alone does not:

- It still wins when a student has a user-level `defaultEnvManager` or
  `defaultInterpreterPath`, which would otherwise beat the auto-pick at
  priorities 2 and 3.
- It needs no popup and no prior state.
- It ignores a stray pick of some system Python, which is stored under a
  different manager.

`python.defaultInterpreterPath` was considered and rejected. The path differs
between `.venv/bin/python` and `.venv\Scripts\python.exe`. A wrong path on one
OS triggers the extension's "settings could not be applied" warning, and the
extension then falls back to auto-discovery anyway.

The entry is not a default. It is the one setting in the folder that overrides
another scope's choice, and its comment says so. `im update` merges it back in
if it goes missing. If a student explicitly picks another interpreter, the
extension rewrites the entry. `im doctor` then reports that the folder's
interpreter is no longer `.venv` and offers to restore it (`im doctor --fix`,
then "Developer: Reload Window").

**2. A documented manual fix**, for when the wrong interpreter shows anyway.
Click the Python version in the status bar (or run "Python: Select
Interpreter" from the Command Palette) and choose the starred `.venv`. The
chapter gives this with a screenshot. For a notebook, the same pick is made
from the kernel name at the top right.

**3. Detection.** The diagnostic block in `widget-check.ipynb` fails loudly
when its kernel is not this folder's `.venv`. `im doctor` checks that the
terminal's `python` is this folder's `.venv`, and that the `pythonProjects`
entry is present and unchanged.

To verify in Phase 5:

- That the workspace folder counts as a project for the priority-1 lookup
  with no other configuration. The lookup needs `projectManager.get(scope)` to
  return the folder.
- That the entry selects `.venv` when the student has first picked a system
  Python.
- That it works with a user-level `defaultInterpreterPath`.
- That it works when `.venv` is created after the folder was opened, with the
  popup dismissed.

## Diagnosing failures

Two facts from the second review shape this section, both tested:

- `uvx` ignores the project's `[tool.uv]`, so `system-certs` in
  `pyproject.toml` does not reach it.
- `uvx` with an empty cache and no network fails outright. The tool meant to
  diagnose the antivirus/TLS case would fail with the same error as step 5.

So there are three layers, from first resort to last:

1. **`im doctor` from the course `.venv`**, in VS Code's terminal (step 8).
   It is already installed and needs no network to start.
2. **`uvx --system-certs --managed-python --from im-course-tools@latest im
   doctor`**, when the environment is broken or missing. The flags are passed
   explicitly because uvx does not read the project's settings (both flags
   exist in uv 0.13, tested). `@latest` stops uvx serving a stale cached `im`.
   On Windows, and in a window where uv is not yet on PATH, the same command
   uses the full path to `uvx`.
3. **`diagnose.sh` / `diagnose.ps1`, shipped in the zip.** The zip arrives
   before uv does, so this is the one diagnostic guaranteed to exist. It needs
   no Python, and it restores the "first check runs without the environment"
   rule that dropping the check scripts gave up. It writes one report file
   that a student mails or shows a TA, containing:
   - `uv --version`, `uv python list --only-installed`, `uv python find`;
   - a verbose `uv sync` into a log;
   - the certificate issuer for pypi.org and github.com (`curl -v` on Mac,
     .NET `SslStream` on Windows), which names an intercepting antivirus;
   - the antivirus products (`Get-CimInstance AntiVirusProduct`) and
     Controlled Folder Access;
   - `Get-ExecutionPolicy -List`;
   - path flags (OneDrive, non-ASCII, length) and free disk space.

## widget-check.ipynb

- **Cell 1 prints one block that answers most tickets from a single
  screenshot:**
  - Python version and architecture;
  - `sys.executable` and the expected `.venv` path, with a match flag;
  - the `home` line from `pyvenv.cfg`, which shows whether the Python is
    uv-managed;
  - the working directory against the course folder (this catches a wrong
    workspace root, together with `notebookFileRoot`);
  - the path flags;
  - the versions of ipywidgets, anywidget, the course widgets and
    im-course-tools;
  - the resolved `jupyter.widgetScriptSources`;
  - a single verdict line.

  It raises a clear error when the kernel is not this folder's `.venv`.
- **Each widget sits under a line saying what should appear.**
- **Blank widgets become visible.** A probe anywidget's JavaScript sets a
  `rendered` trait back to the kernel on render. A later cell prints "front
  end drew widget: True/False", so a widget whose JavaScript failed shows up
  as text a TA can read.
- **The draft is replaced.** The current draft tests `".pixi" in sys.prefix`
  and carries the `instructing-machines` kernelspec; both go.
- **What it cannot detect:** missing extensions (the notebook then cannot run
  at all) and Quarto callouts. The chapter names the missing-extensions
  symptom.

## Phase 1: im-course-tools 0.2.0

Effort: several days plus about a day for the additions below (uvx install
kind, CI mode, `retire-pixi`, the lock and shebang checks). 101 of 296 tests
mention pixi (test_doctor 71, test_cli 19, test_release 9, test_editor 2).

- **`course.py`**: the course folder is the nearest one with a
  `pyproject.toml` whose `[project] name` is `instructing-machines`.
  `url_for` / `DEFAULT_BASE_URL` move to the `uv/` paths.
- **`release.py`, install kinds.**
  - *uv project*: `sys.prefix` named `.venv`, `pyvenv.cfg` containing `uv =`,
    and the course marker in its parent. It is detected before the PIP
    fallback; today a uv `.venv` is misclassified as PIP, and the upgrade runs
    `python -m pip`, which a uv venv lacks (`release.py:224,364`). Its
    self-upgrade fetches the course's new `uv.lock` and runs `uv sync
    --inexact`. If the published lock has not moved, it stays quiet instead of
    looping or failing.
  - *ephemeral uv tool* (running under `uvx`: the prefix is in uv's cache, or
    `UV` is set): never self-upgrades. Otherwise `uvx ... im doctor` would fall
    through to PIP and fail on the missing pip.
  - uv is found in its installer location first, then on PATH. Its version is
    checked against `required-version`, and `im doctor` reports a shadowing uv
    (Homebrew, pip, winget, or an old `~/.cargo/bin`).
- **Windows self-replacement.** A running `im.exe` cannot be replaced: uv
  only self-deletes its own executable (`uv-install-wheel/src/uninstall.rs`),
  and a failure can leave the lock and `.venv` out of step (astral-sh/uv#11134).
  So `im update` renames the running `im.exe` aside before syncing, retries
  once on os error 5, and tells the student to close notebooks. `im doctor`
  detects a half-synced environment with `uv sync --check --inexact`. Tested on
  Windows in CI.
- **`environment.py` (`im update`).**
  - Managed files: `pyproject.toml`, `uv.lock`, `.gitignore`, `.vscode/*`,
    `.im-conflicts.json`, `.pin_shell_path.*`, `diagnose.*`, and
    `widget-check.ipynb`. The notebook is compared with outputs and metadata
    stripped. Without that, every save would make it "differ", and it would be
    replaced and backed up on each run, which is why notebooks were
    deliberately unmanaged until now (`environment.py:111-119`).
  - `ESSENTIAL` becomes `pyproject.toml` and `uv.lock`; `SANITY` checks for
    `[project]` and `version =`.
  - Removed: `CHECK_SCRIPT` (`:56`), `EDITOR_SCRIPT` (`:62`) and their
    `FILES` entries (`:123-124`); `SETUP_TASK` / `DEFINES_SETUP` (`:179-185`)
    and the `pixi run check` handback (`:373-385`); `LOCAL_SETTINGS` / `PINNED`
    (`:154-176`), which are dead once settings are merged.
  - `uv sync --inexact` everywhere `im` syncs, so that packages a student
    installed through a VS Code prompt are not pruned (tested: plain
    `uv sync` removes them). `im doctor` does not flag such extras.
  - **settings.json is merged, not replaced.** Today `put()` overwrites the
    whole file and the single `.backup` (`environment.py:259-271`). Instead,
    published keys are merged into the student's file, with timestamped
    backups.
- **`checks.py`, `doctor.py`, `probe.py`, `security.py`** (the bulk of the work):
  - **Rewritten:** `pixi_check`, `pixi_path_finding`, `environment_check`,
    `moved_check`, `built_for`, `set_by_pixi`, `activation_check`,
    `network_check` (PyPI, files.pythonhosted.org and GitHub for
    python-build-standalone, instead of conda hosts), and the certificate
    verdict, which inverts under `system-certs`.
  - **Deleted:** the `manifest_packages` port. The dependency check compares
    the lock instead: `uv sync --check --inexact` exits 1 on drift (tested).
    `--locked --dry-run` is not used, because it exits 0 on drift (tested).
  - **The moved-folder check** compares the shebang of `.venv/bin/im` (on
    Windows, the trampoline target) with the current `.venv` path. Tested:
    after `mv`, `uv sync` reports everything installed and `uv sync --check`
    exits 0, while every console script fails with "bad interpreter".
  - `vscode_check` stops requiring `munch-group.im-pixi-vscode`
    (`checks.py:140-160, 2429-2445`). It now requires ms-python.python,
    ms-toolsai.jupyter and quarto.quarto, and reports im-pixi-vscode as a
    conflict.
  - `vscode_settings_check` (`checks.py:2558-2640`) drops the kernelspec,
    pinned-path and `useEnvironmentsExtension` checks.
  - **Interpreter check:** the terminal's `python` is this folder's `.venv`,
    and the `pythonProjects` entry is present and names the venv manager.
    `--fix` restores the entry and says to reload the window.
  - **New user-settings check:** flags `python.useEnvironmentsExtension:
    false`, `python.defaultInterpreterPath` and
    `python-envs.defaultEnvManager` in the user `settings.json`, since all
    three beat the `.venv` auto-pick (source).
  - **The checks from the deleted folder scripts move in:** the
    `jupyter.widgetScriptSources` resolution from `.check_vscode.py`. The
    execution-policy report already exists (`checks.py:223, 1500-1580`,
    including Group Policy); only its pixi wording changes.
  - **Path checks** warn when the folder is in OneDrive, longer than about
    60 characters, or not ASCII.
  - The workspace root is checked: the terminal's cwd must be the course
    folder.
  - **`--ci` mode** skips the editor checks, since a CI runner has no VS Code.
  - **Other edits:**
    - `doctor.py`: the PIXI/SHELL gating (`:170`) and the env-var list
      (`:45-47`).
    - Comments in `cli.py:10-14`, `checks.py:49-71`, `checks.py:1783` and
      `editor.py:19`.
    - `checks.py:2570-2626`, which tells students to run `pixi run check`.
    - The cli.py and environment.py docstrings about there being no
      in-environment check now point at the three diagnostic layers.
- **No `im setup`.** There is nothing left to set up.
- **`im retire-pixi [FOLDER...]`**, new. It is run as `uvx --from
  im-course-tools@latest im retire-pixi` (step 5b).
  - **Which folders:** with no argument it finds old course folders itself.
    It recognizes one by a `pixi.toml` whose workspace name is
    `instructing-machines`, or a `.pixi/` beside the course files, and refuses
    anything else.
  - **Confirmation:** it lists what it will do and asks first; `--yes` skips
    the question.
  - **In each folder** it removes `.pixi/`, `pixi.toml`, `pixi.lock`,
    `.pin_pixi_path.py`, the `.backup` copies `im update` made of those, and
    `__pycache__`. Notebooks, data, `week*/` and project folders are never
    touched. On Windows `.pixi` is renamed aside before deletion. Locked files
    are named, with advice to close VS Code. Every step is idempotent.
  - **On the machine:**
    - It uninstalls im-pixi-vscode from every VS Code profile that has it.
    - It removes `python.useEnvironmentsExtension: false` from user
      settings. It flags the other two settings that beat the auto-pick.
      See "Removing im-pixi-vscode".
    - It runs `pixi global uninstall im-course-tools` when that global
      install exists; nothing else in `~/.pixi` is touched. Otherwise the old
      0.1.x `im` in `~/.pixi/bin` wins in any unactivated terminal, and it
      walks into the release-safety trap.
  - **Interpreter choice:** a new folder at the same path as the old pixi
    one inherits VS Code's stored choice for that path, which pointed into
    `.pixi`. Whether that counts as "explicitly chosen" and defeats the
    auto-pick is tested in Phase 5. The documented fallback is "Python:
    Select Interpreter → .venv".
  - **Shell lines:** the PATH lines with the old `pixi run check` marker are
    left alone unless `--shell` is given (they are harmless, and a BSF student
    may rely on them).
  - Tests:
    - a fixture pixi-era folder on each platform;
    - a rerun after a partial failure;
    - a non-course pixi project, which must be refused;
    - a user `settings.json` carrying the global write.
- **Removing im-pixi-vscode.**
  - `munch-group.im-pixi-vscode` goes into `.im-conflicts.json` and into
    `unwantedRecommendations`. `editor.py` already uninstalls listed
    extensions. `im update`, `im doctor` and `im retire-pixi` all run it.
  - The extension can write `python.useEnvironmentsExtension: false` into
    *user* settings: its prompt offers "Set globally"
    (`ConfigurationTarget.Global`, `dist/extension.js` of 0.1.11, read
    locally).
    - That one key is removed when its value is `false`, from the default
      profile's `settings.json` (macOS `~/Library/Application
      Support/Code/User/`, Windows `%APPDATA%\Code\User\`, Linux
      `~/.config/Code/User/`) and from each `User/profiles/*/settings.json`.
    - The edit is made as text, with a timestamped backup.
  - `code --uninstall-extension` acts on one profile at a time, so it runs per
    profile. An extension uninstalled while VS Code runs stays loaded until a
    reload, and the command says so.
  - `editor.py` falls back to the default VS Code install paths when `code`
    is not on PATH, and silently does nothing if VS Code is elsewhere.
    `im doctor` says so.
- `notebooks.py:72` message. Delete the stray caches `get/latest.json` and
  `update/latest.json`.

## Phase 2: the uv student folder

- **`pyproject.toml`**:
  - Contents: the pixi dependency list ported, plus `snippet-cast` and
    `vscodenb`, without `quarto`; a real `description`; no `readme`; no
    build-system (tested: virtual project).
  - `[tool.uv]`:

    ```toml
    [tool.uv]
    required-version = ">=0.11"
    system-certs = true                 # `native-tls` was renamed in uv 0.11
    python-preference = "only-managed"
    required-environments = [
        "sys_platform == 'darwin' and platform_machine == 'arm64'",
        "sys_platform == 'darwin' and platform_machine == 'x86_64'",
        "sys_platform == 'win32' and platform_machine == 'AMD64'",
        "sys_platform == 'linux' and platform_machine == 'x86_64'",
    ]
    ```

    All four keys are accepted without warning and honored from
    `pyproject.toml` (tested). Without `python-preference`, uv happily used a
    pixi Python found on PATH.
  - **Python versions.** `requires-python = ">=3.13,<3.14"` and no
    `.python-version`. Every student gets a uv-managed CPython of the 3.13.x
    line, though not one identical build: uv picks the newest 3.13 already
    installed, `uv.lock` does not pin the patch, and the venv's `home` points
    at the minor-version link (tested). Pin `.python-version` to `3.13.N` only
    if one exact build turns out to matter.
  - **TA overrides,** documented: `UV_PYTHON_PREFERENCE=system` together with
    the python.org installer, when python-build-standalone is blocked or
    quarantined; `UV_PYTHON_INSTALL_DIR`, for a non-ASCII Windows user name.
- **`uv.lock`.** No `.python-version`, no `.env`, no `.check_env.py` or
  `.check_vscode.py`, no `.pin_pixi_path.py`.
- **`diagnose.sh`, `diagnose.ps1`** (see "Diagnosing failures").
- **`.pin_shell_path.sh`, `.pin_shell_path.py`:** ported to `~/.local/bin`
  with a new marker. Nothing runs them. They are managed by `im update`.
- **`widget-check.ipynb`**, rewritten (see its section).
- **`.vscode/extensions.json`**: `recommendations` is `ms-python.python`,
  `ms-toolsai.jupyter` and `quarto.quarto` (im-pixi-vscode used to pull these
  in as dependencies). `unwantedRecommendations` is kept, plus
  `munch-group.im-pixi-vscode`.
- **`.vscode/settings.json`**:
  - Kasper's list, `jupyter.notebookFileRoot`,
    `notebook.output.textLineLimit`, and `jupyter.widgetScriptSources: []`.
    The last is already the default; it is in the folder only to override a
    user-level answer to VS Code's CDN prompt, and its comment says so.
  - `python-envs.pythonProjects` with the `.venv` entry (see "Making `.venv`
    the default interpreter"), with a comment saying why it is there.
  - `files.exclude` lists `.pin_shell_path.*`, `diagnose.*`, `__pycache__`
    and `.pytest_cache`.
  - Nothing else. `python-envs.alwaysUseUv` and
    `python-envs.terminal.autoActivationType` are machine-scoped, so a
    workspace cannot set them. `workspaceSearchPaths` and the interpreter
    settings stay at their defaults. There is no terminal profile.
- **`.gitignore`**: `.venv/`.
- **Clean the draft `student-folder-uv-version/`.** Remove `.git/`,
  `.pixi/`, `pixi.*`, `.pin_pixi_path.py`, `.check_*`, `.python-version`,
  `*.backup`, `.env`, `src/`, the empty `README.md`, and the `settings.json`
  block carrying `/Users/kmt/...` paths.

## Phase 3: build and CI

- **`build_student_folder.py`**:
  - takes a `--template` argument (today `TEMPLATE` is hard-coded to
    `student-folder`);
  - publishes to the `uv/` paths;
  - copies in the `pixi-final` release assets at the old paths;
  - adds `.venv` to `EXCLUDE_DIRS`;
  - asserts the uv zip has no `pixi*`, `.pixi`, `.git`, `.env` or `.check_*`.
- **New workflow, `student-env-check-uv.yml`.**
  - **Trigger:** push, on any branch, touching the uv folder, the workflow
    or the build script. The "Run workflow" button only works for workflows
    already on main.
  - **On all four OSes, using the chapter's own commands:**
    1. Build the zip and unzip it into a temp directory outside the repo.
    2. Use an empty cache. In the git-source phase only, run
       `uv lock --upgrade-package im-course-tools` first.
    3. Run `<full path to uv> sync --locked --directory <folder>`.
    4. Execute `widget-check.ipynb` headless on the `.venv` kernel. This proves
       the kernel, the `sys.prefix` check and every widget import; drawing
       still needs the hand tests.
    5. Run `im doctor --ci` and expect no failures.
    6. On Windows only, the `im update` self-replacement test with `im`
       running.
    7. Run `diagnose.sh` / `diagnose.ps1` and check that the report is
       written.
  - The pixi workflow keeps running alongside until the swap, which retires
    it (it asserts `.pin_pixi_path.py` is in the zip,
    `student-env-check.yml:95-97`).
- **`quarto-publish.yml`.** At the swap, CI loses its Python environment:
  setup-pixi on `student-folder/pixi.toml` feeds the widget-import check,
  `clean_notebooks.py` and Quarto's jupyter engine.
  - Use `astral-sh/setup-uv` and `uv sync --locked --directory
    student-folder`, and put `student-folder/.venv/bin` on `$GITHUB_PATH`.
  - Delete "Register the course kernel" (`:60-70`).
  - Install exactly one Quarto (`quarto-actions/setup` at `:117`).
  - Assert that `jupyter kernelspec list` resolves `python3` into `.venv`.
    `python/course-tools.ipynb` is executed at render time, and without a
    kernelspec Quarto falls back to `python3`.
  - A render-only job runs on the `uv` branch. Deploy is guarded at job level
    (`if: github.ref == 'refs/heads/main'`), with `concurrency:
    pages-${{ github.ref }}`. The branch's `_book` is uploaded as an artifact.
- **Kernel scripts**:
  - `check_notebook_kernels.py` (`CANONICAL_KERNELSPEC`, `drift()`), the
    pre-commit hook and `clean_notebooks.py`'s `normalize` get the `absent`
    mode, and their docstrings are rewritten. `clean_notebooks.py` already
    executes with `BASE_KERNEL="python3"`.
  - `check_env_kernel.py` becomes a check that `python3` resolves into
    `.venv`.
- **Environment drift.** Local `clean-notebooks` runs in the root pixi env,
  while CI runs in the uv env. Add a root task, `clean-notebooks-student`, that
  runs in the uv env, which is authoritative for notebooks.
- **Also port:**
  - `scripts/vscode_kernel_smoketest.sh`, which needs pixi, lists
    im-pixi-vscode and mentions `.check_env.py` (`:87`);
  - `widget_doctor.py`;
  - `.gitattributes` (add a `uv.lock` line).

  Decide whether `scripts/add_vscode_python_envs_setting.py` is kept as is or
  retargeted.

## Phase 4: the chapters (swap-day scripted commit, drafted on the branch)

- **`getting_set_up.qmd`**: the eight steps above.
  - Kept: the platform tabs and the returning-customers callout (fix
    "costumers").
  - Removed: everything about pixi, the terminal restarts, `im --version`,
    `check`, `check-vscode`, and the Mac `code` command step.
  - The "Do not move your student folder" callout becomes the one-command
    recipe: delete `.venv`, then run `uv sync` (full path if needed). A
    moved venv's console scripts keep the old absolute path (tested).
  - The BitDefender paragraph becomes the error table plus the diagnose
    script.
- **`im get/update`** replaces `pixi run get/update`, in VS Code's terminal,
  in:
  - the nine project chapters;
  - `hello-world.qmd`: also its `pixi shell`, and it opens `hello.py` before
    using the terminal. The prompt shows `(instructing-machines)` (tested:
    `pyvenv.cfg` carries `prompt = <project name>`);
  - `intro/notebooks.ipynb`, including its kernel-picking prose, now the
    two-click pick;
  - the slides (`all_slides`, `index`, `week1_mon`).
- **`docs/slides/flashcards.qmd:526-747`**: a rewrite of the pixi deck.
- **Other text:** `docs/_quarto.yml:38,264` comments,
  `scripts/split_notebook_cells.py:19`, the project `CLAUDE.md`.
- **Intentionally left on pixi**:
  - the root `pixi.toml`;
  - `appendix_bsf.ipynb`;
  - `docs/jupyterlite` and `docs/scripts/build-demo.sh`;
  - `python/packages-modules.ipynb:343`;
  - `docs/notes.qmd`.

## Phase 5: verification

- The uv CI workflow is green on all four OSes, from the built zip.
- **By hand**, on fresh Mac and Windows machines (or a fresh VS Code with
  `--user-data-dir` and `--extensions-dir`), following the chapter in its own
  order, with a TestPyPI/wheel im-course-tools. Checks:
  - step 5's full-path sync works straight after the installer;
  - VS Code picks `.venv` on first open, with no "Create environment" offer;
  - the recommended extensions install, and their walkthroughs do not steer
    the student into creating an environment;
  - the first notebook takes exactly two kernel picks;
  - `widget-check.ipynb` draws every widget and reports `rendered: True`;
  - `im doctor` passes in a new terminal;
  - `im update` works on Windows with a notebook open.
- **Variants**:
  - Windows with Smart App Control on;
  - behind a TLS-intercepting proxy, where step 5 fails: check that the error
    table helps, that `diagnose.ps1` names the issuer, and that the `uvx`
    doctor with `--system-certs` runs;
  - a Windows account with a non-ASCII user name (æ/ø/å);
  - a path containing a space;
  - a Mac without the Command Line Tools, where no developer-tools dialog
    should appear;
  - a user `settings.json` from the pixi era, with
    `useEnvironmentsExtension: false`;
  - a new folder at the path of an old pixi folder whose interpreter choice
    VS Code remembers;
  - the four `pythonProjects` checks listed under "Making `.venv` the
    default interpreter";
  - CurrentUser policy set to Restricted, to confirm the extension's
    process-scope policy carries activation;
  - after a Windows feature update, to see whether anything is reset.
- **`uvx --from im-course-tools@latest im retire-pixi`** on real pixi-era
  folders, on Mac and Windows, with VS Code open. Check that:
  - the pixi files are gone;
  - the extension is uninstalled from every profile;
  - the user setting is repaired;
  - the `pixi global` im is removed and the rest of `~/.pixi` untouched;
  - nothing of the student's is touched.
- **`git grep -i pixi`** is reviewed against the "intentionally left" list.

## Decisions log

- 2026-10-10, initial: next cohort only; pixi removal limited to the course's
  own traces; `.venv` kernel; settings.json minimal plus three; root
  `pixi.toml` stays.
- After review round 1: 0.2 on PyPI only; frozen pixi paths after the swap;
  Quarto dropped pending a test; students use VS Code's terminal and plain
  `im`; `.pin_shell_path.*` kept but unused (Mac default-shell mismatch);
  cleanup in a separate `im retire-pixi` that also removes im-pixi-vscode
  and its global user setting.
- Simplification review: S1-S8 adopted (sync before VS Code, full uv path, no
  `im setup` or check scripts, uv-managed Python, minimal settings, one policy
  mechanism, one-command repairs). S9 (`im install`) deferred.
- After review round 2 (this revision):
  - **The Windows policy step is gone entirely.** The Python Environments
    extension sets the process policy itself, so the terminal profile and the
    PowerShell-profile guard are dropped.
  - **A no-Python diagnose script** is added, and the `uvx` doctor gets
    explicit flags and `@latest`.
  - `retire-pixi` no longer converts folders; it also removes the course's
    `pixi global` im. It is step 5b.
  - The download URL moves to `uv/`. The frozen pixi artifacts live in a
    `pixi-final` release.
  - The kernel pick is documented as two clicks.
  - Later, at Kasper's request, `.venv` is made the default interpreter
    without relying on the "new environment" popup. This uses a shipped
    `python-envs.pythonProjects` entry (priority 1 in the extension's
    selection chain), a documented status-bar fix, and `im doctor --fix`.
  - Step 8 runs `im doctor`.
  - Moving the folder requires deleting `.venv`.
  - `uv sync --check --inexact` replaces `--locked --dry-run`.
  - The optional 0.1.30 conda release is cut, because the guard suffices.
  - "Same Python build" is reworded to "same 3.13.x line".

## Out of scope, found along the way

- The pyarmor oracles target darwin.x86_64, linux.x86_64 and windows.x86_64
  only, so they will not load on Apple Silicon (under pixi or uv). Their
  runtime `.so` files are gitignored, and nothing imports `oracle`. Exclude
  `oracle/` from the project zips, or drop the oracles.
- `environment.py`'s `REQUIRED` list omits `vscodenb` and the Quarto CLI.
