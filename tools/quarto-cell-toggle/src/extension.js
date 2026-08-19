'use strict';

const vscode = require('vscode');

const CODE = vscode.NotebookCellKind.Code;
const MARKUP = vscode.NotebookCellKind.Markup;

/** An opening fence: three or more backticks or tildes, then an info string. */
const OPEN_FENCE = /^(`{3,}|~{3,})[ \t]*(.*)$/;

// ---------------------------------------------------------------- config ---

function config() {
  const c = vscode.workspace.getConfiguration('quartoCellToggle');
  return {
    fenceStyle: c.get('fenceStyle', 'plain'),
    runnable: (c.get('runnableLanguages', ['python', 'py', 'r']) || []).map((s) =>
      String(s).toLowerCase()
    ),
    defaultLanguage: c.get('defaultLanguage', 'python'),
    confirmDiscardOutputs: c.get('confirmDiscardOutputs', true),
  };
}

// ---------------------------------------------------------------- fences ---

/**
 * Pull the language out of a fence info string.
 *   "{.python filename=\"Terminal\"}" -> python
 *   "{python}"                        -> python
 *   "python"                          -> python
 *   ""                                -> ''
 */
function parseInfo(info) {
  const raw = String(info || '').trim();
  let s = raw;
  if (s.startsWith('{') && s.endsWith('}')) s = s.slice(1, -1).trim();
  const first = s.split(/\s+/)[0] || '';
  return { raw, lang: first.replace(/^\./, '').toLowerCase() };
}

/**
 * Build an info string for a language, in the configured style.
 *
 * The default is the plain one, ```python, because that is the only spelling
 * a notebook highlights: Jupyter reads the info string as a bare language
 * name, so ```{.python} renders as unhighlighted grey text in the very cells
 * this extension exists to author. Quarto understands all three.
 */
function makeInfo(lang, cfg) {
  const l = lang || cfg.defaultLanguage;
  if (cfg.fenceStyle === 'braced') return `{${l}}`;
  if (cfg.fenceStyle === 'braced-dot') return `{.${l}}`;
  return l;
}

/**
 * True when an info string says nothing that the language name alone does not.
 *   "python", "{python}", "{.python}" -> true
 *   "{.python filename=\"demo.py\"}"  -> false, the attribute is worth keeping
 */
function infoIsJustLanguage(raw) {
  const s = String(raw || '').trim();
  if (!s) return true;
  const lang = parseInfo(s).lang;
  if (!lang) return false;
  const plain = s.toLowerCase();
  return plain === lang || plain === `{${lang}}` || plain === `{.${lang}}`;
}

/**
 * If `text` is exactly one fenced block (blank lines around it are fine),
 * return {info, body, fence}. Otherwise return null - we would rather do
 * nothing than mangle a prose cell.
 */
function parseFencedBlock(text) {
  const lines = String(text).replace(/\s+$/, '').split(/\r?\n/);

  let i = 0;
  while (i < lines.length && lines[i].trim() === '') i++;
  if (i >= lines.length) return null;

  const open = OPEN_FENCE.exec(lines[i]);
  if (!open) return null;

  const fence = open[1];
  const closeRe = new RegExp(`^${fence[0] === '`' ? '`' : '~'}{${fence.length},}[ \\t]*$`);

  // The first closing fence wins; anything but blank lines after it means
  // this cell holds more than a single code block.
  let close = -1;
  for (let j = i + 1; j < lines.length; j++) {
    if (closeRe.test(lines[j])) {
      close = j;
      break;
    }
  }
  if (close === -1) return null;
  for (let j = close + 1; j < lines.length; j++) {
    if (lines[j].trim() !== '') return null;
  }

  return {
    info: parseInfo(open[2]),
    body: lines.slice(i + 1, close).join('\n'),
    fence,
  };
}

/** Long enough not to be closed early by a fence inside the body. */
function pickFence(body) {
  let longest = 0;
  for (const line of String(body).split(/\r?\n/)) {
    // Only a fence at the very start of a line (up to three spaces of
    // indent) can close the block, so backticks inside a string are safe.
    const m = /^ {0,3}(`{3,})/.exec(line);
    if (m) longest = Math.max(longest, m[1].length);
  }
  return '`'.repeat(Math.max(3, longest + 1));
}

// ------------------------------------------------------------ conversion ---

/** Metadata minus our own bookkeeping key. */
function cleanMeta(meta) {
  const out = Object.assign({}, meta || {});
  delete out.quartoFence;
  return out;
}

function codeToMarkup(cell, cfg) {
  const body = cell.document.getText().replace(/\s+$/, '');
  const stored = cell.metadata && cell.metadata.quartoFence;
  // A remembered fence is honoured only when it carries something the language
  // name does not, such as filename="demo.py". A bare {.python} remembered from
  // before is deliberately not restored: it is exactly the spelling this
  // extension is here to migrate away from.
  const keepStored = stored && !infoIsJustLanguage(stored);
  const info = keepStored ? stored : makeInfo(cell.document.languageId, cfg);
  const fence = pickFence(body);

  const data = new vscode.NotebookCellData(
    MARKUP,
    `${fence}${info}\n${body}\n${fence}`,
    'markdown'
  );
  data.metadata = cleanMeta(cell.metadata);
  return data;
}

function markupToCode(cell, cfg, opts) {
  const parsed = parseFencedBlock(cell.document.getText());
  if (!parsed) return { skip: 'this cell is not a single fenced code block' };

  const lang = parsed.info.lang || cfg.defaultLanguage;
  if (!opts.force && parsed.info.lang && !cfg.runnable.includes(lang)) {
    return { skip: `\`${lang}\` is not in quartoCellToggle.runnableLanguages` };
  }

  const data = new vscode.NotebookCellData(CODE, parsed.body, lang === 'py' ? 'python' : lang);
  // Remember the exact fence so the round trip is lossless.
  data.metadata = Object.assign(cleanMeta(cell.metadata), { quartoFence: parsed.info.raw });
  return { data };
}

// -------------------------------------------------------------- commands ---

function selectedIndices(editor) {
  const seen = new Set();
  for (const range of editor.selections) {
    for (let i = range.start; i < range.end; i++) seen.add(i);
  }
  if (seen.size === 0) seen.add(editor.selection.start);
  return [...seen].sort((a, b) => a - b);
}

async function run(direction) {
  const editor = vscode.window.activeNotebookEditor;
  if (!editor) {
    vscode.window.showInformationMessage('Quarto Cell Toggle: no notebook is focused.');
    return;
  }

  const cfg = config();
  const notebook = editor.notebook;
  const indices = selectedIndices(editor);
  const edits = [];
  const skipped = [];
  let losesOutputs = false;

  for (const i of indices) {
    const cell = notebook.cellAt(i);
    const want =
      direction === 'toggle' ? (cell.kind === CODE ? 'toMarkdown' : 'toCode') : direction;

    if (want === 'toMarkdown') {
      if (cell.kind !== CODE) {
        skipped.push(`cell ${i + 1}: already markdown`);
        continue;
      }
      if (cell.outputs && cell.outputs.length > 0) losesOutputs = true;
      edits.push([i, codeToMarkup(cell, cfg)]);
    } else {
      if (cell.kind !== MARKUP) {
        skipped.push(`cell ${i + 1}: already code`);
        continue;
      }
      const res = markupToCode(cell, cfg, { force: direction === 'toCode' });
      if (res.skip) {
        skipped.push(`cell ${i + 1}: ${res.skip}`);
        continue;
      }
      edits.push([i, res.data]);
    }
  }

  if (edits.length === 0) {
    vscode.window.showWarningMessage(
      `Quarto Cell Toggle: nothing to do - ${skipped.join('; ') || 'no cell selected'}.`
    );
    return;
  }

  if (losesOutputs && cfg.confirmDiscardOutputs) {
    const answer = await vscode.window.showWarningMessage(
      'Converting to markdown discards this cell’s outputs and execution count. Continue?',
      { modal: true },
      'Convert'
    );
    if (answer !== 'Convert') return;
  }

  const edit = new vscode.WorkspaceEdit();
  edit.set(
    notebook.uri,
    edits.map(([i, data]) =>
      vscode.NotebookEdit.replaceCells(new vscode.NotebookRange(i, i + 1), [data])
    )
  );
  const ok = await vscode.workspace.applyEdit(edit);
  if (!ok) {
    vscode.window.showErrorMessage('Quarto Cell Toggle: the edit was rejected.');
    return;
  }

  // Replacing a cell clears the selection; put it back where it was.
  editor.selections = edits.map(([i]) => new vscode.NotebookRange(i, i + 1));

  if (skipped.length) {
    vscode.window.showInformationMessage(
      `Quarto Cell Toggle: converted ${edits.length}, skipped ${skipped.length} (${skipped.join('; ')}).`
    );
  }
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('quartoCellToggle.toggle', () => run('toggle')),
    vscode.commands.registerCommand('quartoCellToggle.toCode', () => run('toCode')),
    vscode.commands.registerCommand('quartoCellToggle.toMarkdown', () => run('toMarkdown'))
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
