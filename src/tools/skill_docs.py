from __future__ import annotations

from di_core.registry import registry
from di_skills import skills as _  # noqa: F401 ensure skills are registered


def main() -> None:
    lines = ["| Name | Version | Description |", "| --- | --- | --- |"]
    for name in registry.list():
        cls = registry.get(name)
        doc = (cls.__doc__ or "").strip().replace("\n", " ")
        ver = getattr(cls, "VERSION", "")
        lines.append(f"| {name} | {ver} | {doc} |")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
