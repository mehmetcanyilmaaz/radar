# radar

Personal capability radar: log AI model probe runs by hand, read them back, compare models over time.

```
uv sync
uv run radar probes
uv run radar log --probe <name> --model <name> --verdict pass|partial|fail [--note "..."] [--date YYYY-MM-DD]
uv run radar show --probe <name> [--model <name>]
uv run radar diff --probe <name> --models a,b
```

Probes are defined in PROBES.md. Data lives in store.json. No APIs, no judges — I am the judge; this is the notebook.
