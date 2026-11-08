"""Compute the GPT-2 numbers behind docs/ai/llm.qmd.

The chapter is a guided tour of the Transformer Explainer
(https://poloclub.github.io/transformer-explainer/), which runs GPT-2 small in
the browser.  Every student types the same prompt into it, so the figures and
the answer key can show the numbers the student will see on screen.  Those
numbers come from here, and are saved as a small JSON file that the chapter
reads at render time, so rendering the book needs only matplotlib.

The output probabilities are computed the way the Explainer computes its bars
(src/utils/data.ts in poloclub/transformer-explainer): keep the 50 highest
logits, divide by the temperature, mask all but the top k (or, for top-p, take
softmax over the 50 and keep tokens until the cumulative probability reaches
p), and renormalize over the tokens that are kept.  Block and head numbers in
the JSON are 1-based, as the Explainer labels them.

torch and transformers are deliberately not in the project environment.  Run
it in a throwaway one:

    uv run --with torch --with transformers python scripts/make_llm_data.py
"""

import json
from pathlib import Path

import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

PROMPT = "The virus infects the cell and makes copies of its"
OUT = Path(__file__).resolve().parent.parent / "docs" / "ai" / "data" / "llm-virus.json"

# Words for the embedding-similarity figure; each must be a single token.
SIMILAR_WORDS = [" virus", " bacteria", " cell", " DNA", " RNA", " protein",
                 " car", " truck", " house"]

# The temperatures the Explainer's slider offers that the chapter uses.
TEMPERATURES = [0.2, 0.5, 0.8, 1.0, 2.0, 5.0]
TOP_PS = [0.5, 0.9]


def r(x, n=4):
    return round(float(x), n)


def explainer_top50(logits):
    values, ids = torch.topk(logits, 50)
    return values, ids


def explainer_top_k(values, temperature, k):
    scaled = values / temperature
    masked = torch.full_like(scaled, float("-inf"))
    masked[:k] = scaled[:k]
    return torch.softmax(masked, -1)


def explainer_top_p(values, temperature, p):
    probs = torch.softmax(values / temperature, -1)
    cum = torch.cumsum(probs, -1)
    over = (cum >= p).nonzero()
    cutoff = int(over[0]) if len(over) else len(probs) - 1
    kept = torch.zeros_like(probs)
    kept[: cutoff + 1] = probs[: cutoff + 1]
    return kept / kept.sum()


@torch.no_grad()
def main():
    tok = GPT2TokenizerFast.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", attn_implementation="eager").eval()
    cfg = model.config

    ids = tok(PROMPT, return_tensors="pt").input_ids
    tokens = [tok.decode([i]) for i in ids[0]]
    with torch.no_grad():
        out = model(ids, output_attentions=True, output_hidden_states=True)

    data = {
        "prompt": PROMPT,
        "words": len(PROMPT.split(" ")),
        "tokens": tokens,
        "ids": ids[0].tolist(),
        "n_params": sum(p.numel() for p in model.parameters()),
        "vocab": cfg.vocab_size,
        "dim": cfg.n_embd,
        "blocks": cfg.n_layer,
        "heads": cfg.n_head,
        "mlp_dim": 4 * cfg.n_embd,
        "context": cfg.n_positions,
    }

    # Embedding: the first numbers of a token vector, its position vector and their sum.
    wte, wpe = model.transformer.wte.weight, model.transformer.wpe.weight
    pos = tokens.index(" virus")
    n = 8
    data["embedding"] = {
        "token": " virus",
        "position": pos,
        "token_vec": [r(v) for v in wte[ids[0, pos]][:n]],
        "pos_vec": [r(v) for v in wpe[pos][:n]],
        "sum_vec": [r(v) for v in (wte[ids[0, pos]] + wpe[pos])[:n]],
    }

    # Similarity of token embeddings (cosine).
    sim_ids = []
    for w in SIMILAR_WORDS:
        t = tok(w).input_ids
        assert len(t) == 1, f"{w!r} is {len(t)} tokens"
        sim_ids.append(t[0])
    vecs = torch.nn.functional.normalize(wte[sim_ids], dim=-1)
    data["similarity"] = {
        "words": [w.strip() for w in SIMILAR_WORDS],
        "cosine": [[r(v, 3) for v in row] for row in (vecs @ vecs.T)],
    }

    # Attention: full matrices for the default head and the pronoun head, and
    # the weight from the last token to " virus" in every head.
    att = [a[0] for a in out.attentions]  # per block: heads x query x key
    last = len(tokens) - 1
    data["attention"] = {
        "b1h1": [[r(v, 3) for v in row] for row in att[0][0]],
        "b5h4": [[r(v, 3) for v in row] for row in att[4][3]],
        "last_to_virus": [[r(att[b][h, last, pos], 3) for h in range(cfg.n_head)]
                          for b in range(cfg.n_layer)],
        "last_to_first": [[r(att[b][h, last, 0], 3) for h in range(cfg.n_head)]
                          for b in range(cfg.n_layer)],
    }

    # What the model would predict if it stopped after each block (the
    # "logit lens"): final layer norm and output layer applied to the
    # intermediate vectors of the last token.
    track = {w: tok(w).input_ids[0] for w in (" own", " DNA")}
    lens, lens_track = [], {w.strip(): [] for w in track}
    for b in range(1, cfg.n_layer + 1):
        h = out.hidden_states[b][0, last]
        if b < cfg.n_layer:  # the last hidden state already has ln_f applied
            h = model.transformer.ln_f(h)
        probs = torch.softmax(model.lm_head(h), -1)
        top = torch.topk(probs, 3)
        lens.append([[tok.decode([int(i)]), r(v)] for v, i in zip(top.values, top.indices)])
        for w, i in track.items():
            lens_track[w.strip()].append(r(probs[i]))
    data["logit_lens"] = lens
    data["logit_lens_track"] = lens_track

    # Output layer.
    logits = out.logits[0, last]
    full = torch.softmax(logits, -1)
    top = torch.topk(full, 10)
    data["full_softmax_top10"] = [[tok.decode([int(i)]), r(v)] for v, i in zip(top.values, top.indices)]
    values, top_ids = explainer_top50(logits)
    data["logits_top10"] = [[tok.decode([int(i)]), r(v, 2)] for v, i in zip(values[:10], top_ids[:10])]
    names = [tok.decode([int(i)]) for i in top_ids]
    data["top_k5"] = {}
    for T in TEMPERATURES:
        p = explainer_top_k(values, T, 5)
        data["top_k5"][str(T)] = [[names[i], r(p[i])] for i in range(5)]
    data["top_p"] = {}
    for P in TOP_PS:
        p = explainer_top_p(values, 0.8, P)
        kept = int((p > 0).sum())
        data["top_p"][str(P)] = [[names[i], r(p[i])] for i in range(kept)]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
