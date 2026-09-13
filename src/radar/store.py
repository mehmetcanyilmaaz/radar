"""Data layer: the Run class, the exception family, load/save/append.

Skeleton only — every TODO is yours. Contracts come from RADAR-SPEC-W3.md.
"""

import json  # noqa: F401  (you'll use it; remove the noqa when you do)

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

    TODO __init__: store the six fields; raise RadarError if verdict not in VERDICTS
    TODO __repr__: constructor-call form; truncate response to ~40 chars
    TODO __eq__:   all six fields equal (and return NotImplemented for non-Runs)
    TODO from_dict(cls, d): classmethod, build a Run from a store dict
    TODO to_dict(self): inverse of from_dict
    Contract: Run.from_dict(r.to_dict()) == r   (there's a test for this)
    """


# --- store I/O ------------------------------------------------------------

def load_store(path: str = STORE_PATH) -> dict:
    """Return {"probes": [...], "runs": [Run, ...]}.

    TODO missing file  -> {"probes": DEFAULT_PROBES copy, "runs": []}
    TODO valid JSON    -> parse; convert each run dict via Run.from_dict
    TODO bad JSON/empty-> catch json.JSONDecodeError, raise StoreCorruptedError from it
    """
    raise NotImplementedError


def save_store(store: dict, path: str = STORE_PATH) -> None:
    """Inverse of load_store: Runs back to dicts, json.dump with indent=2."""
    raise NotImplementedError


def add_run(store: dict, run: Run) -> None:
    """Append run to store["runs"].

    TODO run.probe not in store["probes"]            -> UnknownProbeError
    TODO existing run with same (probe, model, date) -> DuplicateRunError
    """
    raise NotImplementedError
