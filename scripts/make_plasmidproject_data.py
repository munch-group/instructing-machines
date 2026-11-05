"""Build the data for the plasmid project (project-files/plasmidproject).

The project hands students the virulence plasmid pO157 of E. coli O157:H7
Sakai (RefSeq NC_002128.1) as sequencing reads, a database of proteins from
related plasmids, and a scorer that knows which ORFs are annotated genes
without showing them. This script makes all three, deterministically:

* plasmid_reads.txt -- the plasmid cut open in the middle of its longest
  intergenic stretch (so no gene is split), then cut into error-free reads
  of 900-1100 bp that overlap their neighbors by 250-400 bp, shuffled and
  renamed. The plasmid's longest exact repeat is 211 bp, so every true
  overlap is longer than any chance one.
* proteins.fasta -- proteins of four related plasmids (F, pWR100, pSLT,
  pB171), dropping pseudogenes, partial proteins, anything under 30 aa, and
  anything close to identical to a pO157 protein, so that homology is
  evidence rather than a lookup of the answer.
* the GENERATED blocks of genescore.py and test_plasmidproject.py -- salted
  hashes of the 85 annotated genes, keyed by strand and stop codon, and the
  expected plasmid and candidate set.

It then checks its own output: the reads must reassemble to the plasmid
with the week-10 greedy algorithm, every annotated stop must be a stop
codon, and every gene must be among the candidates.

Sources are downloaded from NCBI once and cached in scripts/data/plasmidproject/.

    python3 scripts/make_plasmidproject_data.py
"""

from __future__ import annotations

import hashlib
import random
import re
import sys
import time
import urllib.request
from pathlib import Path

from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "scripts" / "data" / "plasmidproject"
PROJECT = REPO / "project-files" / "plasmidproject"

PLASMID = "NC_002128.1"
RELATED = {
    "NC_002483.1": "plasmid F, Escherichia coli K-12",
    "NC_002698.1": "plasmid pWR100, Shigella flexneri",
    "NC_003277.2": "plasmid pSLT, Salmonella Typhimurium",
    "NC_002142.1": "plasmid pB171, enteropathogenic Escherichia coli",
}

SEED = 20261104
READ_LENGTH = (900, 1100)
OVERLAP = (250, 400)
SALT = "pO157-sakai"
# A database protein is dropped when its local alignment score to some pO157
# protein is at least this fraction of the smaller of the two self-scores.
NEAR_IDENTICAL = 0.8

STOPS = {"TAA", "TAG", "TGA"}
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch(accession: str, rettype: str, suffix: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{accession}.{suffix}"
    if not path.exists():
        url = f"{EUTILS}?db=nuccore&id={accession}&rettype={rettype}&retmode=text"
        print(f"downloading {accession} ({rettype})")
        with urllib.request.urlopen(url) as response:
            path.write_bytes(response.read())
        time.sleep(0.5)
    return path


def reverse_complement(seq: str) -> str:
    return seq[::-1].translate(str.maketrans("ACGT", "TGCA"))


def translate(dna: str) -> str:
    from Bio.Seq import Seq
    return str(Seq(dna).translate())


def cut_site(n: int, cds) -> int:
    """Middle of the longest stretch covered by no CDS."""
    covered = [False] * n
    for f in cds:
        for part in f.location.parts:
            for i in range(int(part.start), int(part.end)):
                covered[i] = True
    best, i = (0, 0), 0
    while i < n:
        if covered[i]:
            i += 1
            continue
        j = i
        while j < n and not covered[j]:
            j += 1
        if j - i > best[1] - best[0]:
            best = (i, j)
        i = j
    return (best[0] + best[1]) // 2


def gene_keys(cds, n: int, cut: int) -> set[tuple[str, int]]:
    """(strand, stop) of each CDS, in the coordinates of its own strand of
    the linearized plasmid; stop is the index of the stop codon's first base."""
    keys = set()
    for f in cds:
        if f.location.strand == 1:
            end = (int(f.location.parts[-1].end) - cut) % n or n
            keys.add(("+", end - 3))
        else:
            start = (int(f.location.parts[-1].start) - cut) % n
            keys.add(("-", n - start - 3))
    return keys


def candidates(plasmid: str) -> list[dict]:
    """The candidate universe: on each strand, every stop codon that an
    in-frame ATG reaches, with the longest such ORF."""
    out = []
    for strand, seq in (("+", plasmid), ("-", reverse_complement(plasmid))):
        first_start = {}
        for i in range(len(seq) - 2):
            if seq[i:i + 3] != "ATG":
                continue
            for j in range(i, len(seq) - 2, 3):
                if seq[j:j + 3] in STOPS:
                    first_start.setdefault(j, i)
                    break
        for stop, start in first_start.items():
            out.append({"strand": strand, "start": start, "stop": stop,
                        "protein": translate(seq[start:stop])})
    return out


def make_reads(plasmid: str, rng: random.Random) -> list[str]:
    reads, pos = [], 0
    while True:
        length = rng.randint(*READ_LENGTH)
        if pos + length >= len(plasmid):
            # the last read ends at the end; make sure it is not nested in
            # the one before it
            reads.append(plasmid[pos:])
            break
        reads.append(plasmid[pos:pos + length])
        pos += length - rng.randint(*OVERLAP)
    assert len(reads[-1]) > OVERLAP[1], "last read too short; change SEED"
    return reads


def overlap(left: str, right: str) -> int:
    for i in range(min(len(left), len(right)), 0, -1):
        if left[-i:] == right[:i]:
            return i
    return 0


def check_assembly(named: dict[str, str], plasmid: str) -> int:
    """Greedy assembly as in the week-10 project; returns the largest chance
    overlap so the margin can be reported."""
    ov = {a: {b: overlap(named[a], named[b]) for b in named if b != a} for a in named}
    true_min = OVERLAP[0]
    chance = max(v for a in ov for v in ov[a].values() if v < true_min)
    first = [r for r in named if max(ov[l][r] for l in named if l != r) < true_min]
    assert len(first) == 1, first
    order = first
    while True:
        nxt = max(ov[order[-1]], key=ov[order[-1]].get)
        if ov[order[-1]][nxt] < true_min:
            break
        order.append(nxt)
    seq = "".join(named[r][:-ov[r][order[i + 1]]] for i, r in enumerate(order[:-1]))
    seq += named[order[-1]]
    assert seq == plasmid, "reads do not reassemble to the plasmid"
    return chance


def protein_database(own: list[str]) -> list[tuple[str, str, str]]:
    aligner = PairwiseAligner(mode="local",
                              substitution_matrix=substitution_matrices.load("BLOSUM62"),
                              open_gap_score=-10, extend_gap_score=-0.5)
    own_self = [aligner.score(p, p) for p in own]
    kept = []
    for accession, source in RELATED.items():
        path = fetch(accession, "fasta_cds_aa", "faa")
        for rec in SeqIO.parse(path, "fasta"):
            desc = rec.description
            if "pseudo=true" in desc or "partial=" in desc:
                continue
            protein = str(rec.seq).rstrip("*")
            if len(protein) < 30 or not set(protein) <= set("ACDEFGHIKLMNPQRSTVWY"):
                continue
            self_score = aligner.score(protein, protein)
            if any(aligner.score(protein, o) >= NEAR_IDENTICAL * min(self_score, s)
                   for o, s in zip(own, own_self)):
                continue
            name = re.search(r"\[protein=([^\]]*)\]", desc).group(1)
            kept.append((name, source, protein))
    return kept


def key_hash(strand: str, stop: int) -> str:
    return hashlib.sha256(f"{SALT}:{strand}:{stop}".encode()).hexdigest()[:16]


def candidate_set_hash(cands) -> str:
    text = ",".join(f"{s}:{a}:{b}" for s, a, b in
                    sorted((c["strand"], c["start"], c["stop"]) for c in cands))
    return hashlib.sha256(text.encode()).hexdigest()


def replace_block(path: Path, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"(# BEGIN GENERATED[^\n]*\n).*?(# END GENERATED)", re.S)
    assert pattern.search(text), f"no GENERATED block in {path}"
    path.write_text(pattern.sub(lambda m: m.group(1) + body + m.group(2), text),
                    encoding="utf-8")


def main() -> int:
    rec = SeqIO.read(fetch(PLASMID, "gbwithparts", "gb"), "genbank")
    full = str(rec.seq).upper()
    n = len(full)
    cds = [f for f in rec.features if f.type == "CDS"]
    cut = cut_site(n, cds)
    plasmid = full[cut:] + full[:cut]

    genes = gene_keys(cds, n, cut)
    rc = reverse_complement(plasmid)
    for strand, stop in genes:
        seq = plasmid if strand == "+" else rc
        assert seq[stop:stop + 3] in STOPS, (strand, stop)
    cands = candidates(plasmid)
    universe = {(c["strand"], c["stop"]) for c in cands}
    assert genes <= universe, genes - universe
    n_plus = sum(c["strand"] == "+" for c in cands)

    rng = random.Random(SEED)
    reads = make_reads(plasmid, rng)
    rng.shuffle(reads)
    named = {f"Read{i + 1}": r for i, r in enumerate(reads)}
    chance = check_assembly(named, plasmid)

    with open(PROJECT / "plasmid_reads.txt", "w", encoding="utf-8") as f:
        for name, seq in named.items():
            f.write(f"{name} {seq}\n")

    database = protein_database([f.qualifiers["translation"][0] for f in cds])
    with open(PROJECT / "proteins.fasta", "w", encoding="utf-8") as f:
        for i, (name, source, protein) in enumerate(database, start=1):
            f.write(f">P{i:03d} {name} [{source}]\n")
            for j in range(0, len(protein), 60):
                f.write(protein[j:j + 60] + "\n")

    hashes = sorted(key_hash(s, p) for s, p in genes)
    set_hash = candidate_set_hash(cands)
    lines = ",\n".join(f"    '{h}'" for h in hashes)
    replace_block(PROJECT / "genescore.py",
                  f'SALT = "{SALT}"\n'
                  f"N_CANDIDATES = {len(cands)}\n"
                  f'CANDIDATE_SET_HASH = "{set_hash}"\n'
                  f"GENE_HASHES = {{\n{lines},\n}}\n")
    replace_block(PROJECT / "test_plasmidproject.py",
                  f"PLASMID_LENGTH = {n}\n"
                  f'PLASMID_SHA256 = "{hashlib.sha256(plasmid.encode()).hexdigest()}"\n'
                  f"N_CANDIDATES = {len(cands)}\n"
                  f"N_PLUS = {n_plus}\n"
                  f"N_MINUS = {len(cands) - n_plus}\n"
                  f'CANDIDATE_SET_HASH = "{set_hash}"\n')

    print(f"plasmid {n} bp, cut at {cut} (GenBank position {cut + 1})")
    print(f"{len(reads)} reads, largest chance overlap {chance} bp "
          f"(true overlaps {OVERLAP[0]}-{OVERLAP[1]} bp)")
    print(f"{len(cands)} candidates ({n_plus} +, {len(cands) - n_plus} -), "
          f"{len(genes)} annotated genes, all among them")
    print(f"{len(database)} proteins in proteins.fasta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
