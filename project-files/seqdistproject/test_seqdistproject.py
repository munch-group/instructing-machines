from pytest import approx
from im_pytest import requires


def _approx_nested(actual, expected, abs=1e-4):
    """Compare (possibly nested) lists of numbers element-wise with approx."""
    if isinstance(expected, (list, tuple)):
        assert isinstance(actual, (list, tuple)), \
            "expected a sequence but got {!r}".format(actual)
        assert len(actual) == len(expected), \
            "length {} != expected {}".format(len(actual), len(expected))
        for a, e in zip(actual, expected):
            _approx_nested(a, e, abs=abs)
    elif isinstance(expected, float):
        assert actual == approx(expected, abs=abs)
    else:
        assert actual == expected


@requires("sequence_difference")
def test_sequence_difference(module):
    assert module.sequence_difference('AATT', 'AAAA') == approx(0.5, abs=1e-4)
    assert module.sequence_difference('ATAA', 'AAAA') == approx(0.25, abs=1e-4)
    assert module.sequence_difference('AAAA', 'AAAA') == approx(0.0, abs=1e-4)
    assert module.sequence_difference('AAAA', 'TTTT') == approx(1.0, abs=1e-4)


@requires("jukes_cantor")
def test_jukes_cantor(module):
    assert module.jukes_cantor(0.1) == approx(0.10732563273050497, abs=1e-4)
    assert module.jukes_cantor(0.2) == approx(0.2326161962278796, abs=1e-4)
    assert module.jukes_cantor(0.0) == approx(0.0, abs=1e-4)


@requires("lower_trian_matrix", "sequence_difference", "jukes_cantor")
def test_lower_trian_matrix(module):
    _approx_nested(
        module.lower_trian_matrix(
            ['TAAAAAAAAAAA', 'TTAAAAAAAAAA', 'AAAAAAAAAAGG', 'AAAAAAAAGGGG']),
        [[],
         [0.08833727674228764],
         [0.30409883108112323, 0.4408399986765892],
         [0.6081976621622466, 0.8239592165010822, 0.18848582121067953]])


@requires("lower_trian_matrix", "sequence_difference", "jukes_cantor")
def test_lower_trian_matrix_pair(module):
    _approx_nested(
        module.lower_trian_matrix(['TAAAAAAAAAAA', 'AAAAAAAAGGGG']),
        [[], [0.6081976621622466]])


@requires("find_lowest_cell")
def test_find_lowest_cell_floats(module):
    assert module.find_lowest_cell(
        [[], [0.2], [0.4, 0.3], [0.3, 0.1, 0.4], [0.5, 0.2, 0.5, 0.6]]) == [3, 1]


@requires("find_lowest_cell")
def test_find_lowest_cell_ints(module):
    assert module.find_lowest_cell(
        [[], [2], [4, 3], [3, 1, 4], [5, 2, 5, 6]]) == [3, 1]


@requires("find_lowest_cell")
def test_find_lowest_cell_small(module):
    assert module.find_lowest_cell([[], [0.1]]) == [1, 0]


@requires("link")
def test_link_ints(module):
    assert module.link(4, 6) == approx(5, abs=1e-4)


# Previously shadowed in the original unittest file: a second ``test_link_2``
# method redefined the first, so the ``link(5, 5) == 5`` case never ran. Ported
# here under a distinct name so it actually executes.
@requires("link")
def test_link_equal(module):
    assert module.link(5, 5) == approx(5, abs=1e-4)


@requires("link")
def test_link_floats(module):
    assert module.link(0.4, 0.6) == approx(0.5, abs=1e-4)


@requires("update_table", "link")
def test_update_table(module):
    before = [[], [0.1], [0.3, 0.4], [0.6, 0.8, 0.2]]
    after = [[], [0.35], [0.7, 0.2]]
    module.update_table(before, 1, 0)
    _approx_nested(before, after)


@requires("update_labels")
def test_update_labels(module):
    before = ['A', 'B', 'C', 'D']
    after = ['(A,B)', 'C', 'D']
    module.update_labels(before, 1, 0)
    assert before == after


@requires("cluster", "lower_trian_matrix", "find_lowest_cell",
                       "update_table", "update_labels", "link",
                       "sequence_difference", "jukes_cantor")
def test_cluster(module):
    assert module.cluster(
        ['TAAAAAAAAAAA', 'TTAAAAAAAAAA', 'AAAAAAAAAAGG', 'AAAAAAAAGGGG'],
        ['Henning', 'Preben', 'Mogens', 'Kurt']) == '((Henning,Preben),(Mogens,Kurt))'
