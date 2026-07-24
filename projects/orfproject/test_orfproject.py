"""Tests for the ORF-finding project (ported to pytest).

Every test receives ``sol`` — your solution module — and uses the ``requires``
marker so an unwritten function is reported as "not defined" instead of crashing.
Values are taken verbatim from the original unittest suite.
"""
import pytest

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

GENOME_FILE = "e_coli_O157_H157_str_Sakai.fasta"


# --------------------------------------------------------------------------- #
# Part 1: finding open reading frames
# --------------------------------------------------------------------------- #

@pytest.mark.requires("find_start_positions")
def test_find_start_positions(sol):
    assert isinstance(sol.find_start_positions("AATGA"), list)
    assert isinstance(sol.find_start_positions(""), list)
    assert sol.find_start_positions("AATGAATGTATG") == [1, 5, 9]
    assert sol.find_start_positions("ATGATGATG") == [0, 3, 6]


@pytest.mark.requires("find_next_codon")
def test_find_next_codon(sol):
    assert sol.find_next_codon("AATTTATTT", 0, "TTT") == 6
    assert sol.find_next_codon("AATTTATTT", 2, "TTT") == 2
    assert sol.find_next_codon("AATTTATTT", 1, "TTT") is None


@pytest.mark.requires("find_next_stop_codon")
def test_find_next_stop_codon(sol):
    assert sol.find_next_stop_codon("AAATGAATG", 0) == 3
    assert sol.find_next_stop_codon("TAGTGAATG", 0) == 0
    assert sol.find_next_stop_codon("ATGAATAG", 2) == 5
    assert sol.find_next_stop_codon("ATGAAATAG", 2) is None


@pytest.mark.requires("find_orfs")
def test_find_orfs(sol):
    assert sol.find_orfs("ATGAAATAGAAATGAAATAGTAA") == [[0, 6], [11, 17]]
    assert sol.find_orfs("ATGAATGAAATAGAATGAAA") == [[0, 15], [4, 10]]
    assert sol.find_orfs("AAATGAAAAAAAAAA") == []


# --------------------------------------------------------------------------- #
# Part 2: translation (reused from the translation project)
# --------------------------------------------------------------------------- #

@pytest.mark.requires("codon_map")
def test_codon_map(sol):
    assert sol.codon_map == CODON_MAP


@pytest.mark.requires("translate_codon")
def test_translate_codon(sol):
    assert sol.translate_codon("ATG") == "M"
    assert sol.translate_codon("TAA") == "*"
    assert sol.translate_codon("NNN") == "?"
    assert sol.translate_codon("ACG") == "T"


@pytest.mark.requires("split_codons")
def test_split_codons(sol):
    assert sol.split_codons("AAATTTCCCGGG") == ["AAA", "TTT", "CCC", "GGG"]
    assert sol.split_codons("NNNNNNNNNNNN") == ["NNN", "NNN", "NNN", "NNN"]
    assert sol.split_codons("ATG") == ["ATG"]
    assert sol.split_codons("") == []


@pytest.mark.requires("translate_orf")
def test_translate_orf(sol):
    assert sol.translate_orf("ATGCCCATGTGA") == "MPM*"
    assert sol.translate_orf("ATGATNATGTGA") == "M?M*"
    assert sol.translate_orf("ATGTGA") == "M*"
    assert sol.translate_orf("") == ""


# --------------------------------------------------------------------------- #
# Part 3: putting everything together (uses the genome FASTA file)
# --------------------------------------------------------------------------- #

@pytest.mark.requires("read_genome")
def test_read_genome(sol):
    genome = sol.read_genome(GENOME_FILE)
    assert genome.endswith("CGCCTTAGTAAGTATTTTTC")


@pytest.mark.requires("find_candidate_proteins")
def test_find_candidate_proteins_small(sol):
    assert sol.find_candidate_proteins("AAAATGATGTAGAAAATGATGTAGAAA") == [
        "MM*", "M*", "MM*", "M*",
    ]


@pytest.mark.requires("find_candidate_proteins", "read_genome")
def test_find_candidate_proteins_genome(sol):
    genome = sol.read_genome(GENOME_FILE)
    predicted_first_1k = [
        "MSLCGLKKESLTAASELVTCRE*", "MKRISTTITTTITTTITITITTGNGAG*",
        "MQNVFCGLPIFWKAMPGRGRWPPSSLPPPKSPTTWWR*", "MPGRGRWPPSSLPPPKSPTTWWR*",
        "MLYPISAMPNVFLPNF*", "MPNVFLPNF*", "MSCMALVC*", "MALVC*",
    ]
    assert sol.find_candidate_proteins(genome[:1000]) == predicted_first_1k
