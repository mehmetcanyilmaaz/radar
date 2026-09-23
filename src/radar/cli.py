"""CLI: argparse subcommands -> handler functions -> store.py.

Skeleton only. Wiring shape is given; every handler body is yours.
"""

import argparse
import sys
from datetime import UTC, datetime

from radar import store
from radar.store import (
    VERDICTS,
    RadarError,
    Run,
    UnknownProbeError,
    add_run,
    load_store,
    save_store,
)


def cmd_probes(args) -> int:
    """Print probe names, one per line."""

    store = load_store()
    for probe in store["probes"]:
        print(probe)
    return 0
    

def cmd_log(args) -> int:
    try:
        store = load_store()
        if sys.stdin.isatty():
            print("Paste response, then Ctrl-D:", file=sys.stderr)
        response = sys.stdin.read()
        run_date = args.date or datetime.now(UTC).date().isoformat()
        run = Run(args.probe, args.model, run_date, response.strip(), args.verdict, args.note)

        duplicate = add_run(store, run)
        save_store(store)
    except RadarError as e:
        print(f"radar: {e}", file=sys.stderr)
        return 1

    if duplicate:
        print(f"warning: duplicate run for {run.probe}/{run.model} on {run.date}", file=sys.stderr)
    return 0
    

def cmd_show(args) -> int:
    """All runs for probe (optionally filtered by model), sorted by date.

    Per run: date, model, verdict, note — then response, indented.
    """

    try:
        store = load_store()
        if args.probe not in store["probes"]:
            raise UnknownProbeError(f"Probe '{args.probe}' is not known in the store")
        runs = [run for run in store["runs"] if run.probe == args.probe]
        if args.model:
            runs = [run for run in runs if run.model == args.model]
        runs.sort(key=lambda r: r.date) # sorts the runs by date in ascending order

        for run in runs:
            print(f"{run.date} {run.model} {run.verdict} {run.note}")
            for line in run.response.splitlines():
                print(f"    {line}")
            print()
        return 0
    except RadarError as e:
        print(f"radar: {e}", file=sys.stderr)
        return 1

def cmd_diff(args) -> int:
    """Latest run per model in args.models (comma-separated), stacked with headers."""
    raise NotImplementedError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="radar")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("probes", help="list probe tasks")
    p.set_defaults(func=cmd_probes)

    p = sub.add_parser("log", help="record a run")
    p.add_argument("--probe", required=True, help="probe name")
    p.add_argument("--model", required=True, help="model identifier")
    p.add_argument("--verdict", required=True, choices=VERDICTS, help="verdict string")
    p.add_argument("--note", default="", help="optional note")
    p.add_argument("--date", default=None, help="ISO date; defaults to today")
    # TODO: --probe (required), --model (required),
    #       --verdict (required, choices=VERDICTS), --note (default ""),
    #       --date (default None)
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("show", help="show runs for a probe")
    # TODO: --probe (required), --model (optional)
    p.add_argument("--probe", required=True, help="probe name")
    p.add_argument("--model", help="model identifier")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("diff", help="compare two models on a probe")
    # TODO: --probe (required), --models (required, "a,b")
    p.add_argument("--probe", required=True, help="probe name")
    p.add_argument("--models", required=True, help="comma-separated model identifiers")
    p.set_defaults(func=cmd_diff)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        args.func(args)
    except RadarError as e:
        print(f"radar: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
