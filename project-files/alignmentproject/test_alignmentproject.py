"""
For im-pytest to find the functions to test they must be in a file 
named the same as this one but without the "test_" prefix in the same 
directory as this one.
"""
from pytest import approx
from im_pytest import requires

import itertools

score_matrix = {'A': {'A': 2, 'T': 0, 'G': 0, 'C': 0},
                'T': {'A': 0, 'T': 2, 'G': 0, 'C': 0},
                'G': {'A': 0, 'T': 0, 'G': 2, 'C': 0},
                'C': {'A': 0, 'T': 0, 'G': 0, 'C': 2}}


# --------------------------------------------------------------------------- #
# empty_matrix
# --------------------------------------------------------------------------- #

@requires("empty_matrix")
def test_empty_matrix_1(module):
    assert module.empty_matrix(3, 4) == [[None, None, None, None],
                                      [None, None, None, None],
                                      [None, None, None, None]]


@requires("empty_matrix")
def test_empty_matrix_2(module):
    assert module.empty_matrix(4, 3) == [[None, None, None],
                                      [None, None, None],
                                      [None, None, None],
                                      [None, None, None]]


@requires("empty_matrix")
def test_empty_matrix_3_separate_rows(module):
    # The sub-lists must be *separate* lists, not repeated references to one
    # list, otherwise changing one cell would change a whole column.
    m = module.empty_matrix(3, 3)
    assert all(x is not y for x, y in itertools.combinations(m, 2)), (
        "The rows returned are multiple references to the same list; build "
        "and append a *separate* list for each row."
    )


# --------------------------------------------------------------------------- #
# prepare_dp_matrix 
# --------------------------------------------------------------------------- #

@requires("prepare_dp_matrix")
def test_prepare_dp_matrix_1(module):
    assert module.prepare_dp_matrix(3, 4, -2) == [[0, -2, -4, -6],
                                            [-2, None, None, None],
                                            [-4, None, None, None]]


@requires("prepare_dp_matrix")
def test_prepare_dp_matrix_2(module):
    assert module.prepare_dp_matrix(3, 4, -1) == [[0, -1, -2, -3],
                                            [-1, None, None, None],
                                            [-2, None, None, None]]


@requires("prepare_dp_matrix")
def test_prepare_dp_matrix_3(module):
    assert module.prepare_dp_matrix(4, 3, -2) == [[0, -2, -4],
                                            [-2, None, None],
                                            [-4, None, None],
                                            [-6, None, None]]


@requires("prepare_dp_matrix")
def test_prepare_dp_matrix_4(module):
    assert module.prepare_dp_matrix(3, 3, -2) == [[0, -2, -4],
                                            [-2, None, None],
                                            [-4, None, None]]

# --------------------------------------------------------------------------- #
# prepare_traceback_matrix 
# --------------------------------------------------------------------------- #

@requires("prepare_traceback_matrix")
def test_prepare_traceback_matrix_1(module):
    assert module.prepare_traceback_matrix(3, 4) == [[None, 'L', 'L', 'L'],
                                            ['U', None, None, None],
                                            ['U', None, None, None]]


@requires("prepare_traceback_matrix")
def test_prepare_traceback_matrix_2(module):
    assert module.prepare_traceback_matrix(3, 4) == [[None, 'L', 'L', 'L'],
                                            ['U', None, None, None],
                                            ['U', None, None, None]]


@requires("prepare_traceback_matrix")
def test_prepare_traceback_matrix_3(module):
    assert module.prepare_traceback_matrix(4, 3) == [[None, 'L', 'L'],
                                            ['U', None, None],
                                            ['U', None, None],
                                            ['U', None, None]]


@requires("prepare_traceback_matrix")
def test_prepare_traceback_matrix_4(module):
    assert module.prepare_traceback_matrix(3, 3) == [[None, 'L', 'L'],
                                            ['U', None, None],
                                            ['U', None, None]]


# --------------------------------------------------------------------------- #
# fill_matrices
# --------------------------------------------------------------------------- #

@requires("fill_matrices")
def test_fill_matrices_1(module):
    assert module.fill_matrices("GTC", "GC", score_matrix, -2) == ([[0, -2, -4], [-2, 2, 0], [-4, 0, 2], [-6, -2, 2]],
 [[None, 'L', 'L'], ['U', 'D', 'L'], ['U', 'U', 'D'], ['U', 'U', 'D']])


@requires("fill_matrices")
def test_fill_matrices_2(module):
    assert module.fill_matrices("ATC", "AC", score_matrix, -2) == ([[0, -2, -4], [-2, 2, 0], [-4, 0, 2], [-6, -2, 2]],
 [[None, 'L', 'L'], ['U', 'D', 'L'], ['U', 'U', 'D'], ['U', 'U', 'D']])

# # --------------------------------------------------------------------------- #
# # get_traceback_arrow  (provided verbatim in the write-up)
# # --------------------------------------------------------------------------- #

# @requires("get_traceback_arrow")
# def test_get_traceback_arrow_1(module):
#     assert module.get_traceback_arrow(
#         [[0, -1, -2], [-1, 2, 1], [-2, 1, 2], [-3, 0, 3]],
#         3, 2, 2, -1) == "diagonal"


# @requires("get_traceback_arrow")
# def test_get_traceback_arrow_2(module):
#     assert module.get_traceback_arrow(
#         [[0, -1, -2], [-1, 2, 1], [-2, 1, 2], [-3, 0, 3]],
#         2, 1, 0, -1) == "up"


# @requires("get_traceback_arrow")
# def test_get_traceback_arrow_3(module):
#     assert module.get_traceback_arrow(
#         [[0, -1, -2, -3], [-1, 2, 1, 0], [-2, 1, 2, 3]],
#         1, 2, 0, -1) == "left"


# --------------------------------------------------------------------------- #
# traceback  (provided verbatim in the write-up)
# --------------------------------------------------------------------------- #


@requires("traceback")
def test_traceback_1(module):
    assert module.traceback(
        'AT', 'GAT',
        [[None, 'L', 'L', 'L'], ['U', 'D', 'D', 'L'], ['U', 'D', 'D', 'D']],
        ) == ('-AT', 'GAT')


@requires("traceback")
def test_traceback_2(module):
    assert module.traceback(
        'ATAT', 'GATGAT',  
        [[None, 'L', 'L', 'L', 'L', 'L', 'L'],
  ['U', 'D', 'D', 'L', 'L', 'D', 'L'],
  ['U', 'D', 'D', 'D', 'L', 'L', 'D'],
  ['U', 'D', 'D', 'D', 'D', 'D', 'L'],
  ['U', 'D', 'U', 'D', 'D', 'D', 'D']]) == ('-AT-AT', 'GATGAT')


# --------------------------------------------------------------------------- #
# align
# --------------------------------------------------------------------------- #

@requires("align")
def test_align_1(module):
    assert module.align('GC', 'GTC', score_matrix, -1) == ('G-C', 'GTC')


@requires("align")
def test_align_2(module):
    assert module.align('AT', 'GAT', score_matrix, -1) == ('-AT', 'GAT')


@requires("align")
def test_align_3(module):
    assert module.align('ATAT', 'GATGAT', score_matrix, -1) == ('-AT-AT', 'GATGAT')

# --------------------------------------------------------------------------- #
# align
# --------------------------------------------------------------------------- #

@requires("identity_line")
def identity_line_1(module):
    assert module.identity_line('G-C', 'GTC') == '| |'


@requires("identity_line")
def test_identity_line_2(module):
    assert module.identity_line('AAAA', 'AAAA') == '||||'


@requires("identity_line")
def test_identity_line_3(module):
    assert module.identity_line('ATAT', 'TATA') == '    '


@requires("identity_line")
def test_identity_line_4(module):
    assert module.identity_line('AATAA', '--T--') == '  |  '