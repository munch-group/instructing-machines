"""Tests for the folding / primer-analysis project (ported to pytest).

Every test receives ``sol`` — your solution module — and uses the ``requires``
marker so an unwritten function is reported as "not defined" instead of crashing.
"""
import pytest


@pytest.mark.requires("count_bases")
def test_count_bases(sol):
    assert sol.count_bases('ATGG') == {'A': 1, 'C': 0, 'G': 2, 'T': 1}
    assert sol.count_bases('ATGGCC') == {'A': 1, 'T': 1, 'G': 2, 'C': 2}
    assert sol.count_bases('') == {'A': 0, 'T': 0, 'G': 0, 'C': 0}


@pytest.mark.requires("reverse_complement")
def test_reverse_complement(sol):
    assert sol.reverse_complement('ATGC') == 'GCAT'


@pytest.mark.requires("reverse_complement")
def test_reverse_complement_empty(sol):
    assert sol.reverse_complement('') == ''


@pytest.mark.requires("reverse_complement")
def test_reverse_complement_homopolymer(sol):
    # Previously shadowed by a duplicate `test_reverse_complement_2` name in the
    # original unittest file; ported here under a distinct name so it runs.
    assert sol.reverse_complement('AAAAAAA') == 'TTTTTTT'


@pytest.mark.requires("melting_temp")
def test_melting_temp(sol):
    assert sol.melting_temp('ATG') == pytest.approx(8, abs=1e-4)
    assert sol.melting_temp('AAAAATTTTTCCCCCGGGGG') == pytest.approx(
        51.78000000000001, abs=1e-4)


@pytest.mark.requires("has_hairpin")
def test_has_hairpin(sol):
    assert sol.has_hairpin('ATATCCCCATAT', 4) == True
    assert sol.has_hairpin('ATATCCATAT', 4) == False
    assert sol.has_hairpin('ATCCCCAT', 4) == False
    assert sol.has_hairpin('ATCCCCAT', 2) == True
    assert sol.has_hairpin('GGGGATATCCCCATAT', 4) == True
    assert sol.has_hairpin('GGGGGGATATCCCCCCATAT', 6) == True
