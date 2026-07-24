"""Tests for the seqdist project (ported to pytest).

Every test receives ``sol`` — your solution module — and uses the ``requires``
marker so an unwritten function is reported as "not defined" instead of crashing.

Distances here are ``math.log``-based (Jukes-Cantor), so floats are compared with
``pytest.approx(..., abs=1e-4)``; nested list structures are compared element-wise.
"""
import pytest


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
        assert actual == pytest.approx(expected, abs=abs)
    else:
        assert actual == expected


@pytest.mark.requires("sequence_difference")
def test_sequence_difference(sol):
    assert sol.sequence_difference('AATT', 'AAAA') == pytest.approx(0.5, abs=1e-4)
    assert sol.sequence_difference('ATAA', 'AAAA') == pytest.approx(0.25, abs=1e-4)
    assert sol.sequence_difference('AAAA', 'AAAA') == pytest.approx(0.0, abs=1e-4)
    assert sol.sequence_difference('AAAA', 'TTTT') == pytest.approx(1.0, abs=1e-4)


@pytest.mark.requires("jukes_cantor")
def test_jukes_cantor(sol):
    assert sol.jukes_cantor(0.1) == pytest.approx(0.10732563273050497, abs=1e-4)
    assert sol.jukes_cantor(0.2) == pytest.approx(0.2326161962278796, abs=1e-4)
    assert sol.jukes_cantor(0.0) == pytest.approx(0.0, abs=1e-4)


@pytest.mark.requires("lower_trian_matrix", "sequence_difference", "jukes_cantor")
def test_lower_trian_matrix(sol):
    _approx_nested(
        sol.lower_trian_matrix(
            ['TAAAAAAAAAAA', 'TTAAAAAAAAAA', 'AAAAAAAAAAGG', 'AAAAAAAAGGGG']),
        [[],
         [0.08833727674228764],
         [0.30409883108112323, 0.4408399986765892],
         [0.6081976621622466, 0.8239592165010822, 0.18848582121067953]])


@pytest.mark.requires("lower_trian_matrix", "sequence_difference", "jukes_cantor")
def test_lower_trian_matrix_pair(sol):
    _approx_nested(
        sol.lower_trian_matrix(['TAAAAAAAAAAA', 'AAAAAAAAGGGG']),
        [[], [0.6081976621622466]])


@pytest.mark.requires("find_lowest_cell")
def test_find_lowest_cell_floats(sol):
    assert sol.find_lowest_cell(
        [[], [0.2], [0.4, 0.3], [0.3, 0.1, 0.4], [0.5, 0.2, 0.5, 0.6]]) == [3, 1]


@pytest.mark.requires("find_lowest_cell")
def test_find_lowest_cell_ints(sol):
    assert sol.find_lowest_cell(
        [[], [2], [4, 3], [3, 1, 4], [5, 2, 5, 6]]) == [3, 1]


@pytest.mark.requires("find_lowest_cell")
def test_find_lowest_cell_small(sol):
    assert sol.find_lowest_cell([[], [0.1]]) == [1, 0]


@pytest.mark.requires("link")
def test_link_ints(sol):
    assert sol.link(4, 6) == pytest.approx(5, abs=1e-4)


# Previously shadowed in the original unittest file: a second ``test_link_2``
# method redefined the first, so the ``link(5, 5) == 5`` case never ran. Ported
# here under a distinct name so it actually executes.
@pytest.mark.requires("link")
def test_link_equal(sol):
    assert sol.link(5, 5) == pytest.approx(5, abs=1e-4)


@pytest.mark.requires("link")
def test_link_floats(sol):
    assert sol.link(0.4, 0.6) == pytest.approx(0.5, abs=1e-4)


@pytest.mark.requires("update_table", "link")
def test_update_table(sol):
    before = [[], [0.1], [0.3, 0.4], [0.6, 0.8, 0.2]]
    after = [[], [0.35], [0.7, 0.2]]
    sol.update_table(before, 1, 0)
    _approx_nested(before, after)


@pytest.mark.requires("update_labels")
def test_update_labels(sol):
    before = ['A', 'B', 'C', 'D']
    after = ['(A,B)', 'C', 'D']
    sol.update_labels(before, 1, 0)
    assert before == after


@pytest.mark.requires("cluster", "lower_trian_matrix", "find_lowest_cell",
                       "update_table", "update_labels", "link",
                       "sequence_difference", "jukes_cantor")
def test_cluster(sol):
    assert sol.cluster(
        ['TAAAAAAAAAAA', 'TTAAAAAAAAAA', 'AAAAAAAAAAGG', 'AAAAAAAAGGGG'],
        ['Henning', 'Preben', 'Mogens', 'Kurt']) == '((Henning,Preben),(Mogens,Kurt))'
