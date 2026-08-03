from pytest import approx
from im_pytest import requires

def approx_equal(actual, expected):
    """Recursively compare structures, using approx for floats."""
    if isinstance(expected, dict):
        assert isinstance(actual, dict)
        assert set(actual.keys()) == set(expected.keys())
        for key in expected:
            approx_equal(actual[key], expected[key])
    elif isinstance(expected, (list, tuple)):
        assert type(actual) == type(expected)
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            approx_equal(a, e)
    elif isinstance(expected, float) or isinstance(actual, float):
        assert actual == pytest.approx(expected, abs=1e-4)
    else:
        assert actual == expected


CODON_MAP = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S', 'TCC': 'S',
    'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L',
    'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGT': 'R', 'CGC': 'R',
    'CGA': 'R', 'CGG': 'R', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N',
    'AAA': 'K', 'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A', 'GCC': 'A',
    'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

# The all-zero codon-count dictionary, reused as the count_codons baseline.
ZERO_COUNTS = {codon: 0 for codon in CODON_MAP}


@requires("codon_map")
def test_codon_map_defined(module):
    assert hasattr(module, "codon_map")


@requires("codon_map")
def test_codon_map_unchanged(module):
    assert module.codon_map == CODON_MAP


@requires("split_codons")
def test_split_codons(module):
    assert module.split_codons("AAATTTCCCGGG") == ["AAA", "TTT", "CCC", "GGG"]
    assert module.split_codons("NNNNNNNNNNNN") == ["NNN", "NNN", "NNN", "NNN"]
    assert module.split_codons("ATG") == ["ATG"]
    assert module.split_codons("") == []


@requires("count_codons")
def test_count_codons(module):
    expected1 = dict(ZERO_COUNTS)
    expected1["ATG"] = 1
    expected1["TGA"] = 1
    approx_equal(module.count_codons("ATGTGA"), expected1)

    expected2 = dict(ZERO_COUNTS)
    expected2["ATG"] = 1
    expected2["TCC"] = 4
    expected2["TGA"] = 1
    approx_equal(module.count_codons("ATGTCCTCCTCCTCCTGA"), expected2)


@requires("group_counts_by_amino_acid")
def test_group_counts_by_amino_acid(module):
    input1 = dict(ZERO_COUNTS)
    input1["ATG"] = 1
    input1["TGA"] = 1
    expected1 = {
        'A': {'GCA': 0, 'GCC': 0, 'GCT': 0, 'GCG': 0},
        'C': {'TGC': 0, 'TGT': 0},
        'E': {'GAG': 0, 'GAA': 0},
        'D': {'GAT': 0, 'GAC': 0},
        'G': {'GGT': 0, 'GGG': 0, 'GGA': 0, 'GGC': 0},
        'F': {'TTC': 0, 'TTT': 0},
        'I': {'ATT': 0, 'ATC': 0, 'ATA': 0},
        'H': {'CAC': 0, 'CAT': 0},
        'K': {'AAG': 0, 'AAA': 0},
        '*': {'TAG': 0, 'TGA': 1, 'TAA': 0},
        'M': {'ATG': 1},
        'L': {'CTT': 0, 'CTG': 0, 'CTA': 0, 'CTC': 0, 'TTA': 0, 'TTG': 0},
        'N': {'AAT': 0, 'AAC': 0},
        'Q': {'CAA': 0, 'CAG': 0},
        'P': {'CCT': 0, 'CCG': 0, 'CCA': 0, 'CCC': 0},
        'S': {'TCT': 0, 'AGC': 0, 'TCG': 0, 'AGT': 0, 'TCC': 0, 'TCA': 0},
        'R': {'AGG': 0, 'CGC': 0, 'CGG': 0, 'CGA': 0, 'AGA': 0, 'CGT': 0},
        'T': {'ACC': 0, 'ACA': 0, 'ACG': 0, 'ACT': 0},
        'W': {'TGG': 0},
        'V': {'GTA': 0, 'GTC': 0, 'GTT': 0, 'GTG': 0},
        'Y': {'TAT': 0, 'TAC': 0},
    }
    approx_equal(module.group_counts_by_amino_acid(input1), expected1)

    input2 = dict(ZERO_COUNTS)
    input2["ATG"] = 1
    input2["TCC"] = 4
    input2["TGA"] = 1
    expected2 = {
        'A': {'GCA': 0, 'GCC': 0, 'GCT': 0, 'GCG': 0},
        'C': {'TGC': 0, 'TGT': 0},
        'E': {'GAG': 0, 'GAA': 0},
        'D': {'GAT': 0, 'GAC': 0},
        'G': {'GGT': 0, 'GGG': 0, 'GGA': 0, 'GGC': 0},
        'F': {'TTC': 0, 'TTT': 0},
        'I': {'ATT': 0, 'ATC': 0, 'ATA': 0},
        'H': {'CAC': 0, 'CAT': 0},
        'K': {'AAG': 0, 'AAA': 0},
        '*': {'TAG': 0, 'TGA': 1, 'TAA': 0},
        'M': {'ATG': 1},
        'L': {'CTT': 0, 'CTG': 0, 'CTA': 0, 'CTC': 0, 'TTA': 0, 'TTG': 0},
        'N': {'AAT': 0, 'AAC': 0},
        'Q': {'CAA': 0, 'CAG': 0},
        'P': {'CCT': 0, 'CCG': 0, 'CCA': 0, 'CCC': 0},
        'S': {'TCT': 0, 'AGC': 0, 'TCG': 0, 'AGT': 0, 'TCC': 4, 'TCA': 0},
        'R': {'AGG': 0, 'CGC': 0, 'CGG': 0, 'CGA': 0, 'AGA': 0, 'CGT': 0},
        'T': {'ACC': 0, 'ACA': 0, 'ACG': 0, 'ACT': 0},
        'W': {'TGG': 0},
        'V': {'GTA': 0, 'GTC': 0, 'GTT': 0, 'GTG': 0},
        'Y': {'TAT': 0, 'TAC': 0},
    }
    approx_equal(module.group_counts_by_amino_acid(input2), expected2)


@requires("normalize_counts")
def test_normalize_counts(module):
    approx_equal(
        module.normalize_counts({'ATT': 8, 'ATC': 10, 'ATA': 2}),
        {'ATC': 0.5, 'ATA': 0.1, 'ATT': 0.4},
    )
    assert module.normalize_counts({'ATT': 0, 'ATC': 0, 'ATA': 0}) is None


@requires("normalize_grouped_counts")
def test_normalize_grouped_counts(module):
    base = {
        'A': {'GCA': 0, 'GCC': 0, 'GCT': 0, 'GCG': 0},
        'C': {'TGC': 0, 'TGT': 0},
        'E': {'GAG': 0, 'GAA': 0},
        'D': {'GAT': 0, 'GAC': 0},
        'G': {'GGT': 0, 'GGG': 0, 'GGA': 0, 'GGC': 0},
        'F': {'TTC': 0, 'TTT': 0},
        'I': {'ATT': 0, 'ATC': 0, 'ATA': 0},
        'H': {'CAC': 0, 'CAT': 0},
        'K': {'AAG': 0, 'AAA': 0},
        '*': {'TAG': 0, 'TGA': 1, 'TAA': 0},
        'M': {'ATG': 1},
        'L': {'CTT': 0, 'CTG': 0, 'CTA': 0, 'CTC': 0, 'TTA': 0, 'TTG': 0},
        'N': {'AAT': 0, 'AAC': 0},
        'Q': {'CAA': 0, 'CAG': 0},
        'P': {'CCT': 0, 'CCG': 0, 'CCA': 0, 'CCC': 0},
        'R': {'AGG': 0, 'CGC': 0, 'CGG': 0, 'CGA': 0, 'AGA': 0, 'CGT': 0},
        'T': {'ACC': 0, 'ACA': 0, 'ACG': 0, 'ACT': 0},
        'W': {'TGG': 0},
        'V': {'GTA': 0, 'GTC': 0, 'GTT': 0, 'GTG': 0},
        'Y': {'TAT': 0, 'TAC': 0},
    }

    def with_serine(serine):
        d = {k: dict(v) for k, v in base.items()}
        d['S'] = serine
        return d

    input1 = with_serine({'TCT': 0, 'AGC': 0, 'TCG': 0, 'AGT': 0, 'TCC': 0, 'TCA': 1})
    expected1 = {
        'S': {'AGT': 0.0, 'TCG': 0.0, 'TCT': 0.0, 'TCA': 1.0, 'TCC': 0.0, 'AGC': 0.0},
        '*': {'TAA': 0.0, 'TGA': 1.0, 'TAG': 0.0},
        'M': {'ATG': 1.0},
    }
    approx_equal(module.normalize_grouped_counts(input1), expected1)

    input2 = with_serine({'TCT': 0, 'AGC': 0, 'TCG': 7, 'AGT': 0, 'TCC': 0, 'TCA': 0})
    expected2 = {
        'S': {'AGT': 0.0, 'TCG': 1.0, 'TCT': 0.0, 'TCA': 0.0, 'TCC': 0.0, 'AGC': 0.0},
        '*': {'TAA': 0.0, 'TGA': 1.0, 'TAG': 0.0},
        'M': {'ATG': 1.0},
    }
    approx_equal(module.normalize_grouped_counts(input2), expected2)

    input3 = with_serine({'TCT': 7, 'AGC': 0, 'TCG': 7, 'AGT': 0, 'TCC': 0, 'TCA': 0})
    expected3 = {
        'S': {'AGT': 0.0, 'TCG': 0.5, 'TCT': 0.5, 'TCA': 0.0, 'TCC': 0.0, 'AGC': 0.0},
        '*': {'TAA': 0.0, 'TGA': 1.0, 'TAG': 0.0},
        'M': {'ATG': 1.0},
    }
    approx_equal(module.normalize_grouped_counts(input3), expected3)


@requires("codon_usage")
def test_codon_usage(module):
    approx_equal(
        module.codon_usage("ATGTGA"),
        {'M': {'ATG': 1.0}, '*': {'TAA': 0.0, 'TAG': 0.0, 'TGA': 1.0}},
    )
    approx_equal(
        module.codon_usage("ATGTGCGATCCAAAATTACCGCTTTTATTACTCTGA"),
        {'P': {'CCG': 0.5, 'CCT': 0.0, 'CCA': 0.5, 'CCC': 0.0},
         'D': {'GAT': 1.0, 'GAC': 0.0},
         'L': {'CTC': 0.2, 'TTG': 0.0, 'CTT': 0.2, 'CTG': 0.0, 'TTA': 0.6, 'CTA': 0.0},
         'M': {'ATG': 1.0},
         'K': {'AAA': 1.0, 'AAG': 0.0},
         'C': {'TGC': 1.0, 'TGT': 0.0},
         '*': {'TAA': 0.0, 'TAG': 0.0, 'TGA': 1.0}},
    )
