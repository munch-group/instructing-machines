"""Tests for the pairwise-alignment project (ported to pytest).

Every test receives ``sol`` -- your solution module -- and uses the ``requires``
marker so an unwritten function is reported as "not defined" instead of crashing.

Ported from the original unittest-based ``test_alignmentproject.py``. The
``prepare_matrix`` test class was commented out in the original; it is
re-enabled here so ``prepare_matrix`` is actually covered.
"""
import itertools

import pytest

score_matrix = {'A': {'A': 2, 'T': 0, 'G': 0, 'C': 0},
                'T': {'A': 0, 'T': 2, 'G': 0, 'C': 0},
                'G': {'A': 0, 'T': 0, 'G': 2, 'C': 0},
                'C': {'A': 0, 'T': 0, 'G': 0, 'C': 2}}


# --------------------------------------------------------------------------- #
# empty_matrix
# --------------------------------------------------------------------------- #

@pytest.mark.requires("empty_matrix")
def test_empty_matrix_1(sol):
    assert sol.empty_matrix(3, 4) == [[None, None, None, None],
                                      [None, None, None, None],
                                      [None, None, None, None]]


@pytest.mark.requires("empty_matrix")
def test_empty_matrix_2(sol):
    assert sol.empty_matrix(4, 3) == [[None, None, None],
                                      [None, None, None],
                                      [None, None, None],
                                      [None, None, None]]


@pytest.mark.requires("empty_matrix")
def test_empty_matrix_3_separate_rows(sol):
    # The sub-lists must be *separate* lists, not repeated references to one
    # list, otherwise changing one cell would change a whole column.
    m = sol.empty_matrix(3, 3)
    assert all(x is not y for x, y in itertools.combinations(m, 2)), (
        "The rows returned are multiple references to the same list; build "
        "and append a *separate* list for each row."
    )


# --------------------------------------------------------------------------- #
# prepare_matrix  (re-enabled -- was commented out in the original)
# --------------------------------------------------------------------------- #

@pytest.mark.requires("prepare_matrix")
def test_prepare_matrix_1(sol):
    assert sol.prepare_matrix(3, 4, -2) == [[0, -2, -4, -6],
                                            [-2, None, None, None],
                                            [-4, None, None, None]]


@pytest.mark.requires("prepare_matrix")
def test_prepare_matrix_2(sol):
    assert sol.prepare_matrix(3, 4, -1) == [[0, -1, -2, -3],
                                            [-1, None, None, None],
                                            [-2, None, None, None]]


@pytest.mark.requires("prepare_matrix")
def test_prepare_matrix_3(sol):
    assert sol.prepare_matrix(4, 3, -2) == [[0, -2, -4],
                                            [-2, None, None],
                                            [-4, None, None],
                                            [-6, None, None]]


@pytest.mark.requires("prepare_matrix")
def test_prepare_matrix_4(sol):
    assert sol.prepare_matrix(3, 3, -2) == [[0, -2, -4],
                                            [-2, None, None],
                                            [-4, None, None]]


# --------------------------------------------------------------------------- #
# fill_matrix
# --------------------------------------------------------------------------- #

@pytest.mark.requires("fill_matrix")
def test_fill_matrix_1(sol):
    assert sol.fill_matrix("AT", "GAT", score_matrix, -2) == [[0, -2, -4, -6],
                                                              [-2, 0, 0, -2],
                                                              [-4, -2, 0, 2]]


@pytest.mark.requires("fill_matrix")
def test_fill_matrix_2(sol):
    assert sol.fill_matrix("GTC", "GC", score_matrix, -2) == [[0, -2, -4],
                                                              [-2, 2, 0],
                                                              [-4, 0, 2],
                                                              [-6, -2, 2]]


# --------------------------------------------------------------------------- #
# get_traceback_arrow  (provided verbatim in the write-up)
# --------------------------------------------------------------------------- #

@pytest.mark.requires("get_traceback_arrow")
def test_get_traceback_arrow_1(sol):
    assert sol.get_traceback_arrow(
        [[0, -1, -2], [-1, 2, 1], [-2, 1, 2], [-3, 0, 3]],
        3, 2, 2, -1) == "diagonal"


@pytest.mark.requires("get_traceback_arrow")
def test_get_traceback_arrow_2(sol):
    assert sol.get_traceback_arrow(
        [[0, -1, -2], [-1, 2, 1], [-2, 1, 2], [-3, 0, 3]],
        2, 1, 0, -1) == "up"


@pytest.mark.requires("get_traceback_arrow")
def test_get_traceback_arrow_3(sol):
    assert sol.get_traceback_arrow(
        [[0, -1, -2, -3], [-1, 2, 1, 0], [-2, 1, 2, 3]],
        1, 2, 0, -1) == "left"


# --------------------------------------------------------------------------- #
# trace_back  (provided verbatim in the write-up)
# --------------------------------------------------------------------------- #

@pytest.mark.requires("trace_back")
def test_trace_back_1(sol):
    assert sol.trace_back(
        'GC', 'GTC',
        [[0, -1, -2, -3], [-1, 2, 1, 0], [-2, 1, 2, 3]],
        score_matrix, -1) == ['G-C', 'GTC']


@pytest.mark.requires("trace_back")
def test_trace_back_2(sol):
    assert sol.trace_back(
        'AT', 'GAT',
        [[0, -1, -2, -3], [-1, 0, 1, 0], [-2, -1, 0, 3]],
        score_matrix, -1) == ['-AT', 'GAT']


@pytest.mark.requires("trace_back")
def test_trace_back_3(sol):
    assert sol.trace_back(
        'ATAT', 'GATGAT',
        [[0, -1, -2, -3, -4, -5, -6],
         [-1, 0, 1, 0, -1, -2, -3],
         [-2, -1, 0, 3, 2, 1, 0],
         [-3, -2, 1, 2, 3, 4, 3],
         [-4, -3, 0, 3, 2, 3, 6]],
        score_matrix, -1) == ['-AT-AT', 'GATGAT']


# --------------------------------------------------------------------------- #
# align
# --------------------------------------------------------------------------- #

@pytest.mark.requires("align")
def test_align_1(sol):
    assert sol.align('GC', 'GTC', score_matrix, -1) == ['G-C', 'GTC']


@pytest.mark.requires("align")
def test_align_2(sol):
    assert sol.align('AT', 'GAT', score_matrix, -1) == ['-AT', 'GAT']


@pytest.mark.requires("align")
def test_align_3(sol):
    assert sol.align('ATAT', 'GATGAT', score_matrix, -1) == ['-AT-AT', 'GATGAT']
