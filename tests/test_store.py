"""Store tests. The parametrize table from the spec, as stubs.

Every test writes its own store file into tmp_path (pytest gives you a fresh
temp directory per test — look up the tmp_path fixture, 10 min, docs-not-cheating)
and calls load_store(path) on it. Never touch the real store.json from tests.
"""

import pytest

from radar.store import (
    DEFAULT_PROBES,
    Run,
    StoreCorruptedError,
    UnknownProbeError,
    add_run,
    load_store,
    save_store,
)


def make_run(**overrides):
    """Helper: one valid Run with defaults, fields overridable per test.
    """
    defaults = {
        "probe": "probe1",
        "model": "model1",
        "date": "2024-01-01",
        "response": "some response",
        "verdict": "pass",
        "note": "some note",
    }
    defaults.update(overrides)
    return Run(**defaults)

# --- load cases: one parametrized test ------------------------------------
# TODO @pytest.mark.parametrize over (file_state, expectation):
#   missing file   -> empty structure, DEFAULT_PROBES seeded
#   valid store    -> runs come back as Run objects
#   corrupted      -> file containing '{not json'  -> StoreCorruptedError
#   empty file     -> zero bytes                   -> StoreCorruptedError
# Hint: pytest.raises for the error rows; write the file with tmp_path / "s.json".



# --- individual tests ------------------------------------------------------

@pytest.mark.parametrize("content", ['{not json', '', '42'])
def test_load_rejects_bad_files(tmp_path, content):
    p = tmp_path / "s.json"
    p.write_text(content)
    with pytest.raises(StoreCorruptedError):
        load_store(str(p))

def test_load_missing_file_seeds_defaults(tmp_path):
    p = tmp_path / "nope.json"
    store = load_store(str(p))
    assert store["runs"] == []
    assert store["probes"] == DEFAULT_PROBES

def test_load_valid_file_returns_run_objects(tmp_path):
    p = tmp_path / "s.json"
    r = make_run()
    save_store({"probes": ["probe1"], "runs": [r]}, str(p))
    loaded = load_store(str(p))
    assert loaded["runs"][0] == r
    assert isinstance(loaded["runs"][0], Run)

def test_run_roundtrip():
    """Run.from_dict(r.to_dict()) == r  — this is __eq__ + both converters."""
    run = make_run()
    d = run.to_dict()
    r2 = Run.from_dict(d)
    assert r2 == run


def test_eq_negative():
    """Two runs differing in exactly one field are not equal."""
    run1 = make_run()
    run2 = make_run(response="different response")
    assert run1 != run2


def test_unknown_probe_rejected():
    """add_run with a probe not in store["probes"] raises UnknownProbeError."""
    store = {"probes": ["probe1"], "runs": []}
    run = make_run(probe="unknown_probe")
    with pytest.raises(UnknownProbeError):
        add_run(store, run)


def test_duplicate_returns_flag():
    """add_run with a run that duplicates an existing (probe, model, date) returns True."""
    store = {"probes": ["probe1"], "runs": []}
    run1 = make_run()
    add_run(store, run1)
    run2 = make_run()  # same probe, model, date
    duplicate = add_run(store, run2)
    assert duplicate is True


def test_unicode_response_survives_roundtrip(tmp_path):
    """Response with Karşıyaka + an emoji: save_store then load_store, intact."""
    p = tmp_path / "s.json"
    r = make_run(response="Karşıyaka 🎯")
    save_store({"probes": ["probe1"], "runs": [r]}, str(p))
    loaded = load_store(str(p))
    assert loaded["runs"][0] == r
    assert isinstance(loaded["runs"][0], Run)
    assert "Karşıyaka" in p.read_text(encoding="utf-8")


def test_log_then_show_happy_path(tmp_path):
    p = tmp_path / "s.json"
    store = {"probes": ["probe1"], "runs": []}
    run = make_run()
    duplicate = add_run(store, run)
    assert duplicate is False
    save_store(store, str(p))
    loaded = load_store(str(p))
    assert loaded["runs"][0] == run