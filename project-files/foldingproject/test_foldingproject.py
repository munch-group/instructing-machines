from pytest import approx
from im_pytest import requires


@requires("count_bases")
def test_count_bases(module):
    assert module.count_bases('ATGG') == {'A': 1, 'C': 0, 'G': 2, 'T': 1}
    assert module.count_bases('ATGGCC') == {'A': 1, 'T': 1, 'G': 2, 'C': 2}
    assert module.count_bases('') == {'A': 0, 'T': 0, 'G': 0, 'C': 0}


@requires("reverse_complement")
def test_reverse_complement(module):
    assert module.reverse_complement('ATGC') == 'GCAT'


@requires("reverse_complement")
def test_reverse_complement_empty(module):
    assert module.reverse_complement('') == ''


@requires("reverse_complement")
def test_reverse_complement_homopolymer(module):
    # Previously shadowed by a duplicate `test_reverse_complement_2` name in the
    # original unittest file; ported here under a distinct name so it runs.
    assert module.reverse_complement('AAAAAAA') == 'TTTTTTT'


@requires("melting_temp")
def test_melting_temp(module):
    assert module.melting_temp('ATG') == approx(8, abs=1e-4)
    assert module.melting_temp('AAAAATTTTTCCCCCGGGGG') == approx(
        51.78000000000001, abs=1e-4)


@requires("has_hairpin")
def test_has_hairpin(module):
    assert module.has_hairpin('ATATCCCCATAT', 4) == True
    assert module.has_hairpin('ATATCCATAT', 4) == False
    assert module.has_hairpin('ATCCCCAT', 4) == False
    assert module.has_hairpin('ATCCCCAT', 2) == True
    assert module.has_hairpin('GGGGATATCCCCATAT', 4) == True
    assert module.has_hairpin('GGGGGGATATCCCCCCATAT', 6) == True
