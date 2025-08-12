from __future__ import annotations

import argparse
import inspect
import sys
from pathlib import Path

from di_core.registry import registry
from . import skills  # ensure all skills are registered


def generate_docs() -> str:
    """Generate markdown documentation for all registered skills."""

    lines = ["# Skill Documentation", ""]
    for name in registry.list():
        cls = registry.get(name)
        lines.append(f"## {cls.NAME} (v{cls.VERSION})")
        doc = inspect.getdoc(cls) or ""
        if doc:
            lines.append(doc)
            lines.append("")
        inputs = getattr(cls, "INPUTS", {})
        if inputs:
            lines.append("**Inputs**")
            for k, v in inputs.items():
                lines.append(f"- `{k}`: {v}")
            lines.append("")
        outputs = getattr(cls, "OUTPUTS", {})
        if outputs:
            lines.append("**Outputs**")
            for k, v in outputs.items():
                lines.append(f"- `{k}`: {v}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    """CLI entry point for generating skill documentation."""

    parser = argparse.ArgumentParser(description="Generate skill documentation")
    parser.add_argument(
        "dest",
        nargs="?",
        help="Optional path to write markdown output. If omitted, prints to stdout.",
    )
    args = parser.parse_args()

    content = generate_docs()
    if args.dest:
        path = Path(args.dest)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    else:
        sys.stdout.write(content)


if __name__ == "__main__":
    main()
