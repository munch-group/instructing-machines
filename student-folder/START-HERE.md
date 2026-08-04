# Start here

*Welcome to Instructing Machines. This page gets your machine ready. It takes
about fifteen minutes, most of which is waiting, and you only do it once.*

You are reading this inside the course folder. Everything you need for the
whole term is in here: the data files, the project files, the recipe for the
Python environment, and the two notebooks for week one. The rest of the lecture
notebooks you fetch from the website one at a time as we get to them — there is
a one-line command for it, and you will meet it in step 5.

Work through the five steps below in order. If a step does not do what it says
it will, look at **When something goes wrong** at the bottom before you panic.
Nothing here can break your computer.

---

## 1. Put this folder somewhere sensible

If you have not unzipped it yet, do that now, and put the folder in a plain,
short place that belongs to you:

- **Windows:** `C:\bioprog\` — so you end up with `C:\bioprog\instructing-machines\`
- **Mac:** your home folder — so you end up with `~/bioprog/instructing-machines/`

Three things to avoid, all of which cause trouble later:

- Do not leave it inside `Downloads`. You will lose it.
- Do not put it in OneDrive or iCloud Drive. They sync files in and out from
  under you while Python is reading them, and that produces errors nobody can
  explain.
- Do not use a path with æ, ø, å or spaces in it. Some of the tools we use are
  still not fluent in Danish.

## 2. Install pixi

`pixi` is the program that will install Python for you. It installs one
self-contained Python *per project folder*, so the course Python cannot collide
with any other Python on your machine.

**Windows:** download and run the installer:

<https://github.com/prefix-dev/pixi/releases/latest/download/pixi-x86_64-pc-windows-msvc.msi>

Double-click it and click through. That is all. (If you have one of the rare
ARM-based Windows machines — a Surface Pro X, for instance — use
[pixi-aarch64-pc-windows-msvc.msi](https://github.com/prefix-dev/pixi/releases/latest/download/pixi-aarch64-pc-windows-msvc.msi)
instead.)

**Mac:** open the Terminal app and paste this line, then press Enter:

```
curl -fsSL https://pixi.sh/install.sh | sh
```

**Both:** when it finishes, **close the terminal window and open a new one.** A
program that has just been installed is invisible to terminals that were
already open. This one detail is responsible for more confusion than everything
else on this page combined.

Check that it worked by typing:

```
pixi --version
```

You should see a version number. If you instead see something about the command
not being recognised, see the bottom of this page.

## 3. Open the folder in VS Code

Start VS Code, then choose **File → Open Folder…** and select the
`instructing-machines` folder — the folder itself, not a file inside it.

This matters more than it looks like it does. This folder carries settings that
tell VS Code where the course Python lives, and VS Code only reads them when
the folder is what you opened.

VS Code will show a small notification offering to install the *recommended
extensions* for this folder. Say yes. It is installing Python support, notebook
support, and pixi support. If you miss the notification, open the Extensions
panel on the left and search for `ms-python.python`, `ms-toolsai.jupyter` and
`renan-r-santos.pixi-code`.

## 4. Install the course environment

Inside VS Code, open a terminal with **Terminal → New Terminal**. It opens
already standing in this folder. Type:

```
pixi install
```

Now go and make coffee. The first run downloads a few hundred megabytes and
takes a couple of minutes; it will never take that long again. When it is done
there is a new hidden `.pixi` folder here containing your very own Python.

Then check it:

```
pixi run check
```

It should print a line saying everything is installed, followed by a Python
version. If it does, you are finished with the hard part.

## 5. Run your first notebook

Week one's notebooks are already here. In the file list on the left, open the
`week1` folder and double-click `notebooks-in-vscode.ipynb`.

In the top right of the notebook there is a **Select Kernel** button. Click it,
choose **Python Environments**, and pick the one whose path contains `.pixi` —
it will be the one named after this folder. VS Code remembers your choice for
next time.

Now click the ▶ next to the first code cell. If a number appears in the
brackets beside it, your machine just did what you told it to, and the rest of
the course is detail.

## Getting the rest of the notebooks

Only week one ships in this folder. Every other chapter you fetch when we reach
it, so that the notebook you are working in is always the current version of
the chapter you are reading. In the VS Code terminal, type:

```
pixi run get iteration
```

That downloads the notebook for the chapter called *iteration* and puts it
straight into this folder, ready to open. To see what you can ask for, run it
without a name:

```
pixi run get
```

If you already have a notebook of that name, yours is left exactly as it is and
the fresh copy arrives beside it as `iteration-2.ipynb`. Nothing you have
written is ever overwritten, so it is always safe to ask for a clean copy.

There is also a **Download notebook** button in the margin of every chapter on
the website. It gives you the identical file. The only difference is that it
lands in your Downloads folder and you have to move it here yourself — which is
worth knowing about for the day the terminal is being difficult.

---

## Living in this folder

```
instructing-machines/
├── START-HERE.md      this page
├── pixi.toml          the recipe for your Python environment
├── pixi.lock          the exact versions, so all 100 of us get the same ones
├── get.py             what `pixi run get` runs
├── update.py          what `pixi run update-env` runs
├── week1/             the two notebooks for the first week
├── data/              data files the lecture notes read
├── projects/          the programming projects, one folder each
└── (fetched notebooks land here, at this level)
```

The notes open data files with paths like `data/orfs.csv`, written relative to
this folder rather than to the notebook. So a notebook finds its data whether
it sits at the top level or in a subfolder of your own — that is what the
`week1` folder is quietly demonstrating, and it is why you may make a `week2`
folder and so on if you like a tidy desk. If you would rather not think about
it, leave everything at the top level; that works too.

Your own files, your own notebooks, and anything you write in `projects/` are
yours. Nothing in this folder ever gets overwritten by us unless you are
explicitly told to download a replacement.

## When something goes wrong

**"pixi is not recognized as an internal or external command" (Windows) or
"command not found: pixi" (Mac).** The terminal you are typing in was opened
before pixi was installed. Close it and open a new one. If you are inside VS
Code, quit VS Code entirely and start it again.

**Windows says a script cannot be run, or mentions an execution policy.** You
are running a PowerShell install script. Do not fight with it — use the `.msi`
installer linked in step 2 instead. It needs no permissions of that kind.

**`pixi install` fails part-way, or complains about paths being too long.** The
folder is almost certainly too deep, or inside OneDrive. Move the whole folder
to `C:\bioprog\` and run `pixi install` again.

**VS Code will not offer the right kernel.** Make sure you opened the *folder*
(step 3), that `pixi install` has finished, and that the Python and Jupyter
extensions are installed. Then run **Developer: Reload Window** from the
command palette (Ctrl+Shift+P, or Cmd+Shift+P on a Mac).

**A widget shows as blank space, or as raw text.** You are running the notebook
on the wrong Python. Click **Select Kernel** and choose the `.pixi` one.

**`pixi run get` says it cannot reach the course website.** Either you are
offline or the university network is having a moment. Use the **Download
notebook** button on the chapter page instead and move the file into this
folder by hand. Nothing is lost either way — it is the same notebook.

**Nothing works and the lecture has already started.** Open the course website
and use the in-browser notebooks. They run Python inside the browser with
nothing installed, they are slower and slightly limited, and they will get you
through the next hour. Then come to the study café and we will fix your
installation properly.

---

*If you get stuck on any of this, that is information, not failure. Bring the
exact error message — a screenshot or a copy-paste, not a description of it —
and we will read it together. Reading error messages is one of the things this
course is actually about.*
