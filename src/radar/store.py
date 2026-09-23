"""Data layer: the Run class, the exception family, load/save/append.

Skeleton only — every TODO is yours. Contracts come from RADAR-SPEC-W3.md.
"""

import copy
import json
import os

STORE_PATH = "store.json"
DEFAULT_PROBES = [
    "constraint-stack-v1",
    "policy-pressure-v1",
    "verbatim-fidelity-v1",
]
VERDICTS = ("pass", "partial", "fail")


# --- exceptions -----------------------------------------------------------

class RadarError(Exception):
    """Base for everything this tool raises on purpose. main() catches this."""


class StoreCorruptedError(RadarError):
    pass


class UnknownProbeError(RadarError):
    pass


class DuplicateRunError(RadarError):
    pass


# --- data model -----------------------------------------------------------

class Run:
    """One probe run: probe, model, date (ISO str), response, verdict, note.

    Contract: Run.from_dict(r.to_dict()) == r   (there's a test for this)
    """

    def __init__(self, probe: str, model: str, date: str, response: str, verdict: str, note: str = ""):
        if verdict not in VERDICTS:
            raise RadarError(f"Invalid verdict: {verdict}")
        self.probe = probe
        self.model = model
        self.date = date
        self.response = response
        self.verdict = verdict
        self.note = note

    def __repr__(self) -> str:
        short_response = (self.response[:40] + "…") if len(self.response) > 40 else self.response
        return (
            f"Run(probe={self.probe!r}, model={self.model!r}, date={self.date!r}, "
            f"response={short_response!r}, verdict={self.verdict!r}, note={self.note!r})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Run):
            return NotImplemented
        return (
            self.probe == other.probe and
            self.model == other.model and
            self.date == other.date and
            self.response == other.response and
            self.verdict == other.verdict and
            self.note == other.note
        )

    def to_dict(self) -> dict:
        """Return a dict suitable for JSON storage."""
        return {
            "probe": self.probe,
            "model": self.model,
            "date": self.date,
            "response": self.response,
            "verdict": self.verdict,
            "note": self.note,
        }
    @classmethod
    def from_dict(cls, d: dict) -> "Run":
        """Class method: build a Run from a store dict."""
        return cls(
            probe=d["probe"],
            model=d["model"],
            date=d["date"],
            response=d["response"],
            verdict=d["verdict"],
            note=d["note"],
        )


# --- store I/O ------------------------------------------------------------

def load_store(path: str = STORE_PATH) -> dict:
    """Return {"probes": [...], "runs": [Run, ...]}.
    """

    if not os.path.exists(path):
        return {"probes": copy.deepcopy(DEFAULT_PROBES), "runs": []}

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise StoreCorruptedError(f"Store file is not valid JSON: {path}") from e

    if not isinstance(data, dict):
        raise StoreCorruptedError("Store file does not contain a JSON object")
    
    return {
        "probes": data.get("probes", copy.deepcopy(DEFAULT_PROBES)),
        "runs": [Run.from_dict(run_dict) for run_dict in data.get("runs", [])],
    }




def save_store(store: dict, path: str = STORE_PATH) -> None:
    """Inverse of load_store: Runs back to dicts, json.dump with indent=2."""

    for run in store.get("runs", []):
        if not isinstance(run, Run):
            raise RadarError("All items in store['runs'] must be Run instances")

    data = {
        "probes": store.get("probes"),
        "runs": [run.to_dict() for run in store.get("runs", [])],
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    


def add_run(store: dict, run: Run) -> bool:
    """Append run to store["runs"]. Returns True if it duplicates an existing
    (probe, model, date) — duplicates are allowed, the caller decides whether to warn.

    Raises UnknownProbeError if run.probe isn't in store["probes"].
    """
    known = set(store.get("probes", []))
    if run.probe not in known:
        raise UnknownProbeError(f"Probe '{run.probe}' is not known in the store")

    duplicate = any(
        r.probe == run.probe and r.model == run.model and r.date == run.date
        for r in store.get("runs", [])
    )

    store.setdefault("runs", []).append(run)
    return duplicate

