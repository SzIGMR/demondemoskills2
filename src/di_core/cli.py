from __future__ import annotations
import asyncio
import json
import typer
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime
from di_skills.skills.unscrew import Unscrew  # registers skill via import side-effect

app = typer.Typer(help="di.core MVP CLI")

@app.command("skills")
def skills(cmd: str = typer.Argument("list")):
    from di_core.registry import registry
    if cmd == "list":
        for name in registry.list():
            typer.echo(name)
    else:
        typer.echo("Unknown subcommand. Use: dimonta skills list")

@app.command("exec")
def exec_skill(skill_name: str, params_json: str = "{}"):
    params = json.loads(params_json)
    run_id = f"run-{skill_name.lower()}"
    req = ExecuteRequest(skill_name=skill_name, instance_id=run_id, params=params)
    rt = Runtime()

    async def _main():
        async for st in rt.execute(req):
            typer.echo(f"[{st.phase:>9}] {st.progress_pct:3d}% - {st.message}")

    asyncio.run(_main())

@app.command("abort")
def abort(run_id: str):
    rt = Runtime()
    ok = rt.abort(run_id)
    typer.echo("aborted" if ok else "not found or already finished")

if __name__ == "__main__":
    app()
