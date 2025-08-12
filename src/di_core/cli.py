from __future__ import annotations
import asyncio
import json
from typing import List, Optional
import typer

from di_core.api import ExecuteRequest
from di_core.runtime import Runtime
# Registriert den Beispiel-Skill durch Import (Side-Effect)
from di_skills.skills import unscrew as _  # noqa: F401

app = typer.Typer(help="di.core MVP CLI")
skills_app = typer.Typer(help="Manage skills")
db_app = typer.Typer(help="Inspect database")
app.add_typer(skills_app, name="skills")
app.add_typer(db_app, name="db")

@skills_app.command("list")
def skills_list():
    from di_core.registry import registry
    for name in registry.list():
        typer.echo(name)

@skills_app.command("exec")
def skills_exec(
    skill_name: str = typer.Argument(..., help="Skill name, e.g., Unscrew"),
    params_json: Optional[str] = typer.Option(None, "--json", help="Params as JSON string"),
    params_kv: List[str] = typer.Option(None, "-p", "--param", help="Params as key=value (repeatable)"),
):
    # Params zusammenbauen (JSON und/oder -p key=value)
    params: dict[str, str] = {}
    if params_json:
        parsed = json.loads(params_json)
        if not isinstance(parsed, dict):
            raise typer.BadParameter("--json must be a JSON object")
        params.update({str(k): str(v) for k, v in parsed.items()})
    if params_kv:
        for item in params_kv:
            if "=" not in item:
                raise typer.BadParameter("--param expects key=value")
            k, v = item.split("=", 1)
            params[str(k)] = str(v)

    run_id = f"run-{skill_name.lower()}"
    req = ExecuteRequest(skill_name=skill_name, instance_id=run_id, params=params)
    rt = Runtime()

    async def _main():
        async for st in rt.execute(req):
            typer.echo(f"[{st.phase:>9}] {st.progress_pct:3d}% - {st.message}")

    asyncio.run(_main())

@skills_app.command("abort")
def skills_abort(instance_id: str):
    rt = Runtime()
    ok = rt.abort(instance_id)
    typer.echo("aborted" if ok else "not found or already finished")


@db_app.command("show")
def db_show():
    """Print current contents of the database."""
    rt = Runtime()
    typer.echo(json.dumps(rt._dbase.dump(), indent=2))

if __name__ == "__main__":
    app()
