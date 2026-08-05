'use strict';

// Exercises the fence parsing and the two conversions without a running VS Code.
// A stub `vscode` module is injected into the require cache first.

const Module = require('module');
const path = require('path');
const assert = require('assert');

const stub = {
  NotebookCellKind: { Markup: 1, Code: 2 },
  NotebookCellData: class {
    constructor(kind, value, languageId) {
      this.kind = kind;
      this.value = value;
      this.languageId = languageId;
      this.metadata = undefined;
    }
  },
  NotebookRange: class {
    constructor(start, end) {
      this.start = start;
      this.end = end;
    }
  },
  NotebookEdit: { replaceCells: (range, cells) => ({ range, cells }) },
  WorkspaceEdit: class {
    set() {}
  },
  Uri: {},
  window: {
    activeNotebookEditor: undefined,
    showInformationMessage() {},
    showWarningMessage() {},
    showErrorMessage() {},
  },
  commands: { registerCommand: () => ({ dispose() {} }) },
  workspace: {
    getConfiguration: () => ({ get: (key, dflt) => dflt }),
    applyEdit: async () => true,
  },
};

const origLoad = Module._load;
Module._load = function (request, parent, isMain) {
  if (request === 'vscode') return stub;
  return origLoad.apply(this, arguments);
};

// Re-read the source and eval it so the private helpers are reachable.
const fs = require('fs');
const src = fs.readFileSync(path.join(__dirname, '..', 'src', 'extension.js'), 'utf8');
const sandbox = { require, module: { exports: {} }, exports: {} };
const fn = new Function('require', 'module', 'exports', src + '\n;return {parseFencedBlock, parseInfo, makeInfo, pickFence, codeToMarkup, markupToCode, config};');
const api = fn(require, sandbox.module, sandbox.exports);

const { parseFencedBlock, parseInfo, makeInfo, pickFence, codeToMarkup, markupToCode } = api;
const cfg = { fenceStyle: 'braced-dot', runnable: ['python', 'py', 'r'], defaultLanguage: 'python', confirmDiscardOutputs: true };

const cell = (text, meta, languageId) => ({
  document: { getText: () => text, languageId: languageId || 'markdown' },
  metadata: meta,
});

let pass = 0;
function ok(name, f) {
  f();
  pass++;
  console.log('  ok  ' + name);
}

console.log('info strings');
ok('class attribute', () => assert.strictEqual(parseInfo('{.python}').lang, 'python'));
ok('with attributes', () =>
  assert.strictEqual(parseInfo('{.txt filename="Terminal"}').lang, 'txt'));
ok('quarto executable', () => assert.strictEqual(parseInfo('{python}').lang, 'python'));
ok('plain', () => assert.strictEqual(parseInfo('python').lang, 'python'));
ok('empty', () => assert.strictEqual(parseInfo('').lang, ''));

console.log('fence blocks');
ok('simple block', () => {
  const p = parseFencedBlock('```{.python}\nx = 1\nprint(x)\n```');
  assert.strictEqual(p.body, 'x = 1\nprint(x)');
  assert.strictEqual(p.info.lang, 'python');
});
ok('blank lines around', () => {
  const p = parseFencedBlock('\n\n```python\nx = 1\n```\n\n');
  assert.strictEqual(p.body, 'x = 1');
});
ok('prose before is refused', () =>
  assert.strictEqual(parseFencedBlock('Some prose.\n\n```python\nx = 1\n```'), null));
ok('prose after is refused', () =>
  assert.strictEqual(parseFencedBlock('```python\nx = 1\n```\n\nSome prose.'), null));
ok('two blocks refused', () =>
  assert.strictEqual(parseFencedBlock('```python\na\n```\n\n```python\nb\n```'), null));
ok('unclosed refused', () => assert.strictEqual(parseFencedBlock('```python\nx = 1'), null));
ok('pure prose refused', () => assert.strictEqual(parseFencedBlock('Just a sentence.'), null));
ok('four-backtick fence with inner fence', () => {
  const p = parseFencedBlock('````{.python}\n```\nnot a close\n```\n````');
  assert.strictEqual(p.body, '```\nnot a close\n```');
});
ok('tilde fence', () => {
  const p = parseFencedBlock('~~~python\nx = 1\n~~~');
  assert.strictEqual(p.body, 'x = 1');
});

console.log('code -> markdown');
ok('wraps in braced-dot fence', () => {
  const d = codeToMarkup(cell('x = 1\nprint(x)\n', undefined, 'python'), cfg);
  assert.strictEqual(d.value, '```{.python}\nx = 1\nprint(x)\n```');
  assert.strictEqual(d.languageId, 'markdown');
});
ok('honours a remembered fence', () => {
  const d = codeToMarkup(
    cell('ls -l\n', { quartoFence: '{.txt filename="Terminal"}' }, 'python'),
    cfg
  );
  assert.ok(d.value.startsWith('```{.txt filename="Terminal"}\n'));
  assert.strictEqual(d.metadata.quartoFence, undefined);
});
ok('backticks inside a string do not lengthen the fence', () => {
  const d = codeToMarkup(cell('print("```")', undefined, 'python'), cfg);
  assert.strictEqual(d.value, '```{.python}\nprint("```")\n```');
});
ok('lengthens the fence when a line starts with one', () => {
  const d = codeToMarkup(cell('doc = """\n```\n"""', undefined, 'python'), cfg);
  assert.ok(d.value.startsWith('````{.python}'));
  assert.ok(d.value.endsWith('\n````'));
});

console.log('markdown -> code');
ok('unwraps python', () => {
  const r = markupToCode(cell('```{.python}\nx = 1\n```'), cfg, { force: false });
  assert.strictEqual(r.data.value, 'x = 1');
  assert.strictEqual(r.data.languageId, 'python');
  assert.strictEqual(r.data.metadata.quartoFence, '{.python}');
});
ok('leaves a terminal transcript alone', () => {
  const r = markupToCode(cell('```{.txt filename="Terminal"}\n$ ls\n```'), cfg, { force: false });
  assert.ok(r.skip, 'expected a skip');
  assert.ok(/runnableLanguages/.test(r.skip));
});
ok('force converts it anyway', () => {
  const r = markupToCode(cell('```{.txt filename="Terminal"}\n$ ls\n```'), cfg, { force: true });
  assert.strictEqual(r.data.value, '$ ls');
});
ok('refuses a prose cell', () => {
  const r = markupToCode(cell('## A heading\n\nSome prose.'), cfg, { force: true });
  assert.ok(r.skip);
});

console.log('round trip');
ok('markdown -> code -> markdown is identity', () => {
  const original = '```{.python filename="demo.py"}\nfor i in range(3):\n    print(i)\n```';
  const code = markupToCode(cell(original), cfg, { force: false }).data;
  const back = codeToMarkup(
    cell(code.value, code.metadata, code.languageId),
    cfg
  );
  assert.strictEqual(back.value, original);
});
ok('code -> markdown -> code is identity', () => {
  const body = 'def f(x):\n    return x * 2\n\nprint(f(21))';
  const md = codeToMarkup(cell(body, undefined, 'python'), cfg);
  const code = markupToCode(cell(md.value, md.metadata), cfg, { force: false }).data;
  assert.strictEqual(code.value, body);
});

console.log(`\n${pass} assertions passed`);
Module._load = origLoad;
