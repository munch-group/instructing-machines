from pytest import approx
from im_pytest import requires

# --------------------------------------------------------------------------- #
# Load the data the tests need, independently of the student's read_data, from
# the same bare filenames the original test used (files sit in the working dir).
# --------------------------------------------------------------------------- #

def _read_data(file_name):
    with open(file_name) as f:
        return [line.strip() for line in f]


unknown_list = _read_data('unknown_type.txt')
typed_data = {
    'A': _read_data('subtypeA.txt'),
    'B': _read_data('subtypeB.txt'),
    'C': _read_data('subtypeC.txt'),
    'D': _read_data('subtypeD.txt'),
}


# --------------------------------------------------------------------------- #
# Compute the similarity of two sequences
# --------------------------------------------------------------------------- #

@requires("sequence_similarity")
def test_sequence_similarity(module):
    assert module.sequence_similarity('AGTC', 'AGTT') == approx(0.75, abs=1e-4)
    assert module.sequence_similarity('AAAA', 'AAAA') == approx(1.0, abs=1e-4)
    assert module.sequence_similarity('ACGT', 'TGCA') == approx(0.0, abs=1e-4)
    assert module.sequence_similarity('ACGTACGTACGT', 'ACGTACGTACGT') == approx(1.0, abs=1e-4)
    assert module.sequence_similarity('AAAAAAAAAAAA', 'AAAAAAAAAAAT') == approx(11 / 12, abs=1e-4)


@requires("alignment_similarity")
def test_alignment_similarity(module):
    # gap-in-both columns are ignored: 'A-CT-A' vs 'A-CTTA' -> 4 matches / 5 cols
    assert module.alignment_similarity('A-CT-A', 'A-CTTA') == approx(0.8, abs=1e-4)
    assert module.alignment_similarity('A-A-A-A', 'AA-A-AA') == approx(2 / 7, abs=1e-4)
    assert module.alignment_similarity('A-----A', 'AA-A-AA') == approx(2 / 5, abs=1e-4)


# --------------------------------------------------------------------------- #
# Read the HIV sequences into your program
# --------------------------------------------------------------------------- #

@requires("read_data")
def test_read_data(module):
    a = module.read_data('subtypeA.txt')
    assert len(a) == 5 and all(type(x) is str for x in a)
    b = module.read_data('subtypeB.txt')
    assert len(b) == 4 and all(type(x) is str for x in b)
    c = module.read_data('subtypeC.txt')
    assert len(c) == 4 and all(type(x) is str for x in c)
    d = module.read_data('subtypeD.txt')
    assert len(d) == 4 and all(type(x) is str for x in d)


@requires("load_typed_sequences")
def test_load_typed_sequences(module):
    d = module.load_typed_sequences()
    assert isinstance(d, dict)
    assert len(d) == 4
    for key in ('A', 'B', 'C', 'D'):
        assert key in d, '{} is not a key in the returned dictionary'.format(key)
    assert all(type(x) is list for x in d.values()), \
        'The values in the dictionary are not all lists'


# --------------------------------------------------------------------------- #
# Compare your HIV sequence to HIV sequences of known subtype
# --------------------------------------------------------------------------- #

@requires("get_similarities")
def test_get_similarities_lengths(module):
    assert len(module.get_similarities(unknown_list[0], typed_data['A'][0:1])) == 1
    assert len(module.get_similarities(unknown_list[0], typed_data['A'][0:2])) == 2
    assert len(module.get_similarities(unknown_list[0], typed_data['A'])) == 5


@requires("get_similarities")
def test_get_similarities_values(module):
    assert module.get_similarities('ACGT', ['ACGT', 'ACCT', 'TGCA']) == \
        approx([1.0, 0.75, 0.0], abs=1e-4)


# --------------------------------------------------------------------------- #
# Compute maximum similarity to each subtype
# --------------------------------------------------------------------------- #

@requires("get_max_similarities")
def test_get_max_similarities_shape(module):
    res = module.get_max_similarities(unknown_list[0], typed_data)
    assert isinstance(res, dict)
    assert len(res) == 4
    for key in ('A', 'B', 'C', 'D'):
        assert key in res


@requires("get_max_similarities")
def test_get_max_similarities_values(module):
    s = module.get_max_similarities(unknown_list[0], typed_data)
    assert s['A'] == approx(0.8721742704480066, abs=1e-4)
    assert s['B'] == approx(0.8286861234675057, abs=1e-4)
    assert s['C'] == approx(0.8232432432432433, abs=1e-4)
    assert s['D'] == approx(0.8365436349940816, abs=1e-4)


# --------------------------------------------------------------------------- #
# Identify the HIV subtype
# --------------------------------------------------------------------------- #

@requires("predict_subtype")
def test_predict_subtype(module):
    assert module.predict_subtype(unknown_list[0], typed_data) == 'A'
    assert module.predict_subtype(typed_data['A'][0], typed_data) == 'A'
    assert module.predict_subtype(typed_data['B'][0], typed_data) == 'B'
    assert module.predict_subtype(typed_data['C'][0], typed_data) == 'C'
    assert module.predict_subtype(typed_data['D'][0], typed_data) == 'D'


@requires("predict_subtype")
def test_predict_subtype_with_gaps(module):
    i, n = 100, 10
    assert module.predict_subtype(
        typed_data['A'][0][:i] + ' ' * n + typed_data['A'][0][i + n:], typed_data) == 'A'
    i, n = 100, 10
    assert module.predict_subtype(
        typed_data['B'][0][:i] + ' ' * n + typed_data['B'][0][i + n:], typed_data) == 'B'
    i, n = 200, 5
    assert module.predict_subtype(
        typed_data['C'][0][:i] + ' ' * n + typed_data['C'][0][i + n:], typed_data) == 'C'
    i, n = 300, 15
    assert module.predict_subtype(
        typed_data['D'][0][:i] + ' ' * n + typed_data['D'][0][i + n:], typed_data) == 'D'
