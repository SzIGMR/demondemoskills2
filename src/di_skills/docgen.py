from __future__ import annotations
import inspect
from pathlib import Path
from di_core.registry import registry
from . import skills  # ensure all skills are registered


def generate_docs(dest: Path) -> str:
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
    content = "\n".join(lines).strip() + "\n"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)
    return content


def main() -> None:
    doc_path = Path(__file__).resolve().parents[2] / "docs" / "skills.md"
    generate_docs(doc_path)


if __name__ == "__main__":
    main()
