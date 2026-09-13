"""Store tests. The parametrize table from the spec, as stubs.

Every test writes its own store file into tmp_path (pytest gives you a fresh
temp directory per test — look up the tmp_path fixture, 10 min, docs-not-cheating)
and calls load_store(path) on it. Never touch the real store.json from tests.
"""

import pytest  # noqa: F401

# from radar.store import (Run, load_store, save_store, add_run,
#                          StoreCorruptedError, UnknownProbeError, DuplicateRunError)


def make_run(**overrides):
    """Helper: one valid Run with defaults, fields overridable per test.

    TODO: build a Run with sensible defaults, apply overrides, return it.
    Saves you re-typing six fields in every test below.
    """
    raise NotImplementedError


# --- load cases: one parametrized test ------------------------------------
# TODO @pytest.mark.parametrize over (file_state, expectation):
#   missing file   -> empty structure, DEFAULT_PROBES seeded
#   valid store    -> runs come back as Run objects
#   corrupted      -> file containing '{not json'  -> StoreCorruptedError
#   empty file     -> zero bytes                   -> StoreCorruptedError
# Hint: pytest.raises for the error rows; write the file with tmp_path / "s.json".


# --- individual tests ------------------------------------------------------

def test_run_roundtrip():
    """Run.from_dict(r.to_dict()) == r  — this is __eq__ + both converters."""
    raise NotImplementedError


def test_eq_negative():
    """Two runs differing in exactly one field are not equal."""
    raise NotImplementedError


def test_unknown_probe_rejected():
    raise NotImplementedError


def test_duplicate_probe_model_date_rejected():
    raise NotImplementedError


def test_unicode_response_survives_roundtrip():
    """Response with Karşıyaka + an emoji: save_store then load_store, intact."""
    raise NotImplementedError


def test_log_then_show_happy_path():
    """add_run, save, load: the run is there and equal to what went in."""
    raise NotImplementedError
