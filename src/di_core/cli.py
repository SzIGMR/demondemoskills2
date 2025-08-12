from __future__ import annotations

import argparse
from typing import Dict

from di_core.api import Request
from di_core.registry import list_skills
from di_core.runtime import execute


def _parse_params(items: list[str]) -> Dict[str, str]:
    params: Dict[str, str] = {}
    for item in items:
        key, _, value = item.partition("=")
        params[key] = value
    return params


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="di-cli")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List available skills")

    exec_p = sub.add_parser("execute", help="Execute a skill")
    exec_p.add_argument("name")
    exec_p.add_argument("--param", action="append", default=[], help="key=value pairs")

    args = parser.parse_args(argv)
    if args.command == "list":
        for name in list_skills():
            print(name)
        return 0

    if args.command == "execute":
        request = Request(name=args.name, params=_parse_params(args.param))
        status = execute(request)
        print(status)
        return 0 if status.success else 1

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
