"""Throwaway: generate a synthetic radar store for profiling."""

import random
import sys

from radar.store import DEFAULT_PROBES, VERDICTS, Run, save_store

MODELS = ["model-a", "model-b", "model-c", "model-d", "model-e"]
WORDS = ["the", "model", "response", "follows", "each", "instruction", "but", "the", "constraint", "on", "output", "format", "was", "ignored", "in", "the", "second", "section", "while", "policy", "text", "stayed", "intact", "and", "the", "user", "request", "was", "answered", "with", "a", "summary", "table", "plus", "extra", "notes"]


def fake_response(rng: random.Random, n_words: int) -> str:
    return " ".join(rng.choice(WORDS) for _ in range(n_words))


def make_store(n_runs: int, seed: int = 0) -> dict:
    rng = random.Random(seed)
    runs = [
        Run(
            probe=rng.choice(DEFAULT_PROBES),
            model=rng.choice(MODELS),
            date=f"2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            response=fake_response(rng, rng.randint(200, 500)),  # realistic length
            verdict=rng.choice(VERDICTS),
            note="",
        )
        for _ in range(n_runs)
    ]
    return {"probes": list(DEFAULT_PROBES), "runs": runs}


if __name__ == "__main__":
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    save_store(make_store(n), path)
    print(f"wrote {n} runs to {path}")