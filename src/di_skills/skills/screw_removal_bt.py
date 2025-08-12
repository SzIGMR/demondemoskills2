from __future__ import annotations
from typing import Dict, Callable, Iterable, Any
from di_skills.base import Skill, SkillContext, register
from di_core.registry import registry

class Node:
    async def run(self, ctx: SkillContext, memory: Dict[str, Any]) -> None:  # pragma: no cover - interface
        raise NotImplementedError

class Sequence(Node):
    def __init__(self, children: Iterable[Node]):
        self.children = list(children)

    async def run(self, ctx: SkillContext, memory: Dict[str, Any]) -> None:
        for child in self.children:
            await child.run(ctx, memory)

class SkillNode(Node):
    def __init__(self, name: str, param_fn: Callable[[Dict[str, Any]], Dict[str, str]], on_result: Callable[[Dict[str, Any], Dict[str, str], Dict[str, str]], None] | None = None):
        self.name = name
        self.param_fn = param_fn
        self.on_result = on_result

    async def run(self, ctx: SkillContext, memory: Dict[str, Any]) -> None:
        params = self.param_fn(memory)
        skill_cls = registry.get(self.name)
        skill = skill_cls()
        await skill.precheck(ctx, params)
        outputs = await skill.execute(ctx, params)
        memory[self.name] = outputs
        if self.on_result:
            self.on_result(memory, params, outputs)

class ForEach(Node):
    def __init__(self, items_fn: Callable[[Dict[str, Any]], Iterable[str]], node_builder: Callable[[str], Node]):
        self.items_fn = items_fn
        self.node_builder = node_builder

    async def run(self, ctx: SkillContext, memory: Dict[str, Any]) -> None:
        for item in self.items_fn(memory):
            node = self.node_builder(item)
            await node.run(ctx, memory)


@register
class ScrewRemovalWorkflow(Skill):
    """Run detection, planning and removal of all screws using a behavior tree."""

    NAME = "ScrewRemovalWorkflow"
    VERSION = "1.0.0"
    INPUTS = {
        "image_path": "Path to the camera image",
        "torque": "Torque in Nm"
    }
    OUTPUTS = {"removed_ids": "Comma separated removed screw identifiers"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        if not params.get("image_path"):
            raise ValueError("param 'image_path' is required")
        await ctx.status("workflow ready", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        torque = params.get("torque", str(ctx.config.skills.Unscrew.default_torque))
        memory: Dict[str, Any] = {"torque": torque}

        tree = Sequence([
            SkillNode("DetectScrews", lambda m: {"image_path": params["image_path"]}),
            SkillNode("DismantlingPlanner", lambda m: {}),
            ForEach(
                lambda m: [sid for sid in m.get("DismantlingPlanner", {}).get("plan", "").split(",") if sid],
                lambda sid: Sequence([
                    SkillNode("LocateScrew", lambda m, sid=sid: {"screw_id": sid}),
                    SkillNode(
                        "Unscrew",
                        lambda m, sid=sid: {"target_id": sid, "torque": m["torque"]},
                        on_result=lambda m, p, r, sid=sid: m.setdefault("removed", []).append(sid),
                    ),
                ]),
            ),
        ])

        await tree.run(ctx, memory)
        removed = memory.get("removed", [])
        await ctx.status("workflow complete", 95)
        return {"removed_ids": ",".join(removed)}
