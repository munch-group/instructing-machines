"""Tests for the assembly project (ported to pytest).

Every test receives ``sol`` — your solution module — and uses the ``requires``
marker so an unwritten function is reported as "not defined" instead of crashing.

The suite deliberately keeps the original strengths: order-independence checks
(``find_first_read`` is tested against two differently-ordered overlap dicts)
and no-false-overlap checks (pairs that do not overlap must give ``""`` / ``0``).
"""
import pytest

# --------------------------------------------------------------------------- #
# Shared fixtures / expected values (verbatim from the original suite).
# --------------------------------------------------------------------------- #

test_reads = {
    'Read1': 'GGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTCGTCCAGACCCCTAGC',
    'Read6': 'TGACAGTAGATCTCGTCCAGACCCCTAGCTGGTACGTCTTCAGTAGAAAATTGTTTTTTTCTTCCAAGAGGTCGGAGT',
    'Read2': 'CTTTACCCGGAAGAGCGGGACGCTGCCCTGCGCGATTCCAGGCTCCCCACGGG',
    'Read5': 'CGATTCCAGGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTC',
    'Read4': 'TGCGAGGGAAGTGAAGTATTTGACCCTTTACCCGGAAGAGCG',
    'Read3': 'GTCTTCAGTAGAAAATTGTTTTTTTCTTCCAAGAGGTCGGAGTCGTGAACACATCAGT',
}

test_overlaps1 = {
    'Read1': {'Read6': 29, 'Read5': 1, 'Read4': 0, 'Read3': 0, 'Read2': 1},
    'Read3': {'Read1': 0, 'Read5': 0, 'Read6': 1, 'Read4': 1, 'Read2': 0},
    'Read2': {'Read1': 13, 'Read5': 21, 'Read6': 0, 'Read3': 1, 'Read4': 0},
    'Read5': {'Read1': 39, 'Read4': 0, 'Read6': 14, 'Read3': 0, 'Read2': 1},
    'Read6': {'Read1': 0, 'Read5': 0, 'Read4': 1, 'Read3': 43, 'Read2': 0},
    'Read4': {'Read1': 1, 'Read5': 2, 'Read6': 0, 'Read3': 1, 'Read2': 17},
}

# Same content as test_overlaps1 but the reads (and their inner keys) appear in a
# different order -- used to prove find_first_read does not depend on dict order.
test_overlaps2 = {
    'Read3': {'Read1': 0, 'Read5': 0, 'Read6': 1, 'Read4': 1, 'Read2': 0},
    'Read5': {'Read1': 39, 'Read4': 0, 'Read6': 14, 'Read3': 0, 'Read2': 1},
    'Read4': {'Read1': 1, 'Read5': 2, 'Read6': 0, 'Read3': 1, 'Read2': 17},
    'Read2': {'Read1': 13, 'Read5': 21, 'Read6': 0, 'Read3': 1, 'Read4': 0},
    'Read6': {'Read1': 0, 'Read5': 0, 'Read4': 1, 'Read3': 43, 'Read2': 0},
    'Read1': {'Read6': 29, 'Read5': 1, 'Read4': 0, 'Read3': 0, 'Read2': 1},
}

test_print = """       Read1 Read2 Read3 Read4 Read5 Read6
 Read1     -     1     0     0     1    29
 Read2    13     -     1     0    21     0
 Read3     0     0     -     1     0     1
 Read4     1    17     1     -     2     0
 Read5    39     1     0     0     -    14
 Read6     0     0    43     1     0     -
"""

test_first_read = 'Read4'

test_read_order = ['Read4', 'Read2', 'Read5', 'Read1', 'Read6', 'Read3']

test_genome = 'TGCGAGGGAAGTGAAGTATTTGACCCTTTACCCGGAAGAGCGGGACGCTGCCCTGCGCGATT' \
              'CCAGGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTCGTCCAGACCCCTAGCTGGTA' \
              'CGTCTTCAGTAGAAAATTGTTTTTTTCTTCCAAGAGGTCGGAGTCGTGAACACATCAGT'


# --------------------------------------------------------------------------- #
# Part 1: read and analyse the reads
# --------------------------------------------------------------------------- #

@pytest.mark.requires("read_data")
def test_read_data(sol):
    reads = sol.read_data('sequencing_reads.txt')
    assert isinstance(reads, dict)
    assert reads == test_reads


@pytest.mark.requires("mean_length")
def test_mean_length(sol):
    assert sol.mean_length({'Read1': 'ACGT', 'Read2': 'ACGTACGT'}) == pytest.approx(6, abs=1e-4)
    assert sol.mean_length({'Read1': 'ACGTTGCA', 'Read2': 'ACGTACGT'}) == pytest.approx(8, abs=1e-4)
    assert sol.mean_length(
        {'Read1': 'atttaatgtgata', 'Read2': 'agtgtatgatagtacgcgcgc'}
    ) == pytest.approx(17, abs=1e-4)


# --------------------------------------------------------------------------- #
# Part 2: overlaps
# --------------------------------------------------------------------------- #

@pytest.mark.requires("get_overlap")
def test_get_overlap(sol):
    assert sol.get_overlap("AAAAATTTTT", "TTTTTTTTTT") == "TTTTT"
    # no-false-overlap: same reads in the wrong orientation must not overlap
    assert sol.get_overlap("TTTTTTTTTT", "AAAAATTTTT") == ""
    assert sol.get_overlap(
        "TGCGAGGGAAGTGAAGTATTTGACCCTTTACCCGGAAGAGC",
        "CTTTACCCGGAAGAGCGGGACGCTGCCCTGCGCGATTCCAGGCTCCCCACGGG",
    ) == "CTTTACCCGGAAGAGC"
    assert sol.get_overlap(
        "CTTTACCCGGAAGAGCGGGACGCTGCCCTGCGCGATTCCAGGCTCCCCACGGG",
        "CGATTCCAGGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCT",
    ) == "CGATTCCAGGCTCCCCACGGG"
    # no-false-overlap for a real read pair in the wrong orientation
    assert sol.get_overlap(
        "CTTTACCCGGAAGAGCGGGACGCTGCCCTGCGCGATTCCAGGCTCCCCACGGG",
        "TGCGAGGGAAGTGAAGTATTTGACCCTTTACCCGGAAGAGC",
    ) == ""
    assert sol.get_overlap(
        "TGCGAGGGAAGTGAAGTATTTGACCCTTTACCCGGAAGAGCG",
        "CGATTCCAGGCTCCCCACGGGGTACCCATAACTTGACAGTAGATCTC",
    ) == "CG"


@pytest.mark.requires("get_all_overlaps")
def test_get_all_overlaps(sol):
    assert sol.get_all_overlaps(
        {'Read1': "AAAAATTTTT", 'Read2': "TTTTTTTTTA"}
    ) == {'Read1': {'Read2': 5}, 'Read2': {'Read1': 1}}
    assert sol.get_all_overlaps(test_reads) == test_overlaps1


@pytest.mark.requires("pretty_print")
def test_pretty_print(sol, capsys):
    sol.pretty_print(test_overlaps1)
    captured = capsys.readouterr()
    assert captured.out == test_print


# --------------------------------------------------------------------------- #
# Part 3: order of reads
# --------------------------------------------------------------------------- #

@pytest.mark.requires("get_left_overlaps")
def test_get_left_overlaps(sol):
    assert sol.get_left_overlaps(test_overlaps1, test_first_read) == [0, 0, 0, 1, 1]
    assert sol.get_left_overlaps(test_overlaps1, 'Read1') == [0, 0, 1, 13, 39]


@pytest.mark.requires("find_first_read")
def test_find_first_read(sol):
    # order-independence: same overlaps, two different dict orderings
    assert sol.find_first_read(test_overlaps1) == test_first_read
    assert sol.find_first_read(test_overlaps2) == test_first_read


@pytest.mark.requires("find_key_for_largest_value")
def test_find_key_for_largest_value(sol):
    assert sol.find_key_for_largest_value({'A': 3, 'B': 5, 'C': 2}) == 'B'
    assert sol.find_key_for_largest_value(test_overlaps1['Read5']) == 'Read1'


@pytest.mark.requires("find_order_of_reads")
def test_find_order_of_reads(sol):
    assert sol.find_order_of_reads(
        'A', {'C': {'A': 0, 'B': 2}, 'A': {'B': 15, 'C': 1}, 'B': {'A': 0, 'C': 11}}
    ) == ['A', 'B', 'C']
    assert sol.find_order_of_reads('Read4', test_overlaps1) == test_read_order


# --------------------------------------------------------------------------- #
# Part 4: reconstruct the genome
# --------------------------------------------------------------------------- #

@pytest.mark.requires("reconstruct_sequence")
def test_reconstruct_sequence(sol):
    assert sol.reconstruct_sequence(
        ['Read1', 'Read2'],
        {'Read1': "AAAAATTTTT", 'Read2': "TTTTTTTTTA"},
        {'Read1': {'Read2': 5}, 'Read2': {'Read1': 1}},
    ) == 'AAAAATTTTTTTTTA'
    assert sol.reconstruct_sequence(test_read_order, test_reads, test_overlaps1) == test_genome


@pytest.mark.requires("assemble_genome")
def test_assemble_genome(sol):
    assert sol.assemble_genome('sequencing_reads.txt') == test_genome
