"""The `seqtools` module used as the running example in packages-modules.ipynb.

This is the same `gc_content` function the chapter's own `seqtools.py`
listing walks the reader through writing. It exists on disk here so that
the chapter's `%%sandbox` cells can actually `import seqtools` and show
real output, instead of only describing what such an import would do.
"""


def gc_content(dna):
    "Fraction of the bases that are G or C."
    gc = dna.count('G') + dna.count('C')
    return gc / len(dna)
