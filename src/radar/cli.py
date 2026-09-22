"""CLI: argparse subcommands -> handler functions -> store.py.

Skeleton only. Wiring shape is given; every handler body is yours.
"""

import argparse
import sys

from radar.store import RadarError  # plus whatever else you need


def cmd_probes(args) -> None:
    """Print probe names, one per line."""
    raise NotImplementedError


def cmd_log(args) -> None:
    """Read response from stdin until EOF, build a Run, add_run, save.

    Print "Paste response, then Ctrl-D:" first.
    Date: args.date or today (datetime.date.today().isoformat()).
    """
    raise NotImplementedError


def cmd_show(args) -> None:
    """All runs for probe (optionally filtered by model), sorted by date.

    Per run: date, model, verdict, note — then response, indented.
    """
    raise NotImplementedError


def cmd_diff(args) -> None:
    """Latest run per model in args.models (comma-separated), stacked with headers."""
    raise NotImplementedError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="radar")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("probes", help="list probe tasks")
    p.set_defaults(func=cmd_probes)

    p = sub.add_parser("log", help="record a run")
    # TODO: --probe (required), --model (required),
    #       --verdict (required, choices=VERDICTS), --note (default ""),
    #       --date (default None)
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("show", help="show runs for a probe")
    # TODO: --probe (required), --model (optional)
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("diff", help="compare two models on a probe")
    # TODO: --probe (required), --models (required, "a,b")
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
