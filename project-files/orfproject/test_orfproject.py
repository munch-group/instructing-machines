from pytest import approx
from im_pytest import requires

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

@requires("find_start_positions")
def test_find_start_positions(module):
    assert isinstance(module.find_start_positions("AATGA"), list)
    assert isinstance(module.find_start_positions(""), list)
    assert module.find_start_positions("AATGAATGTATG") == [1, 5, 9]
    assert module.find_start_positions("ATGATGATG") == [0, 3, 6]


@requires("find_next_codon")
def test_find_next_codon(module):
    assert module.find_next_codon("AATTTATTT", 0, "TTT") == 6
    assert module.find_next_codon("AATTTATTT", 2, "TTT") == 2
    assert module.find_next_codon("AATTTATTT", 1, "TTT") is None


@requires("find_next_stop_codon")
def test_find_next_stop_codon(module):
    assert module.find_next_stop_codon("AAATGAATG", 0) == 3
    assert module.find_next_stop_codon("TAGTGAATG", 0) == 0
    assert module.find_next_stop_codon("ATGAATAG", 2) == 5
    assert module.find_next_stop_codon("ATGAAATAG", 2) is None


@requires("find_orfs")
def test_find_orfs(module):
    assert module.find_orfs("ATGAAATAGAAATGAAATAGTAA") == [[0, 6], [11, 17]]
    assert module.find_orfs("ATGAATGAAATAGAATGAAA") == [[0, 15], [4, 10]]
    assert module.find_orfs("AAATGAAAAAAAAAA") == []


# --------------------------------------------------------------------------- #
# Part 2: translation (reused from the translation project)
# --------------------------------------------------------------------------- #

@requires("codon_map")
def test_codon_map(module):
    assert module.codon_map == CODON_MAP


@requires("translate_codon")
def test_translate_codon(module):
    assert module.translate_codon("ATG") == "M"
    assert module.translate_codon("TAA") == "*"
    assert module.translate_codon("NNN") == "?"
    assert module.translate_codon("ACG") == "T"


@requires("split_codons")
def test_split_codons(module):
    assert module.split_codons("AAATTTCCCGGG") == ["AAA", "TTT", "CCC", "GGG"]
    assert module.split_codons("NNNNNNNNNNNN") == ["NNN", "NNN", "NNN", "NNN"]
    assert module.split_codons("ATG") == ["ATG"]
    assert module.split_codons("") == []


@requires("translate_orf")
def test_translate_orf(module):
    assert module.translate_orf("ATGCCCATGTGA") == "MPM*"
    assert module.translate_orf("ATGATNATGTGA") == "M?M*"
    assert module.translate_orf("ATGTGA") == "M*"
    assert module.translate_orf("") == ""


# --------------------------------------------------------------------------- #
# Part 3: putting everything together (uses the genome FASTA file)
# --------------------------------------------------------------------------- #

@requires("read_genome")
def test_read_genome(module):
    genome = module.read_genome(GENOME_FILE)
    assert genome.endswith("CGCCTTAGTAAGTATTTTTC")


@requires("find_candidate_proteins")
def test_find_candidate_proteins_small(module):
    assert module.find_candidate_proteins("AAAATGATGTAGAAAATGATGTAGAAA") == [
        "MM*", "M*", "MM*", "M*",
    ]


@requires("find_candidate_proteins", "read_genome")
def test_find_candidate_proteins_genome(module):
    genome = module.read_genome(GENOME_FILE)
    predicted_first_1k = [
        "MSLCGLKKESLTAASELVTCRE*", "MKRISTTITTTITTTITITITTGNGAG*",
        "MQNVFCGLPIFWKAMPGRGRWPPSSLPPPKSPTTWWR*", "MPGRGRWPPSSLPPPKSPTTWWR*",
        "MLYPISAMPNVFLPNF*", "MPNVFLPNF*", "MSCMALVC*", "MALVC*",
    ]
    assert module.find_candidate_proteins(genome[:1000]) == predicted_first_1k
