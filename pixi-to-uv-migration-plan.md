## New UV setup

Basically just use `uv` as dropin replacement for `pixi` and drop the `im-pixi-vscode` extension. That way everything becomes "native" vscode and the student can safely follow the instructions for any extension recommendations and missing dependencies.

Update `im-course-tool` and `.pin_shell_path.sh` to use `uv` instead of `pixi`.

`pixi install` would be `uv sync`.

`pixi shell` would not needed if they *only* use the VScode terminal (I could tell them to do so).

In `vscode/extensions.json`, `"recommendations": ["munch-group.im-pixi-vscode"],` must be removed.

New `vscode/settings.json`:

```json
{
    "chat.disableAIFeatures": true,
    "files.exclude": {
        "**/.pin_pixi_path.py": true,
        "**/.pin_shell_path.py": true,
        "**/.check_env.py": true,
        "**/.check_vscode.py": true,
        "**/__pycache__": true,
        "**/.pytest_cache": true
    },
    "editor.inlineSuggest.edits.allowCodeShifting": "never",
    "editor.inlineSuggest.edits.renderSideBySide": "never",
    "editor.acceptSuggestionOnEnter": "off",
    "editor.snippetSuggestions": "none",
    "workbench.welcomePage.walkthroughs.openOnInstall": false,
}
```

Install uv on Mac:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# maybe to make sure:
# Add to Zsh (macOS default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
# Add to Bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
```

On mac maybe change `sh` to $SHELL or $(dscl . -read ~ UserShell | sed 's/UserShell: //')

Install Windows:

```txt
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Generate env:

```bash
uv sync

# force reinstall and do not rely on cached deps info
uv sync --reinstall --refresh
```

```bash
# if folder is moved:
rm -rf .venv ; uv sync
```

To switch from pixi to uv:

- Add `.python-version`, `.env`, and `pyproject.toml`
- Remove `pixi.toml` and `pixi.lock`
- Make CI use `uv.lock` instead of `pixi.lock`
- Change `vscode/extensions.json` and `vscode/settings.json`
- Install `uv` and pin paths
- Make students use `im update` and `im get` in stead of the the `pixi run` versions.
- Make `im update` remove all pixi and the `im-course-tools extension`.
