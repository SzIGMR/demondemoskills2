# Demo Skills Framework

Minimal framework for registering and executing skills. Includes example
skills for detecting, locating and unscrewing screws as well as a simple
`DismantlingPlanner`. A tiny runtime with CLI support persists data via a
miniature `di.base` database which can be inspected using `dimonta db show`.

## Installation

Install the latest version directly from GitHub:

```bash
pip install git+https://github.com/SzIGMR/demondemoskills2.git
```

This provides the `dimonta` CLI for running and inspecting skills and a
`skill-docs` helper to regenerate the documentation in `docs/skills.md`.

## Usage

List the available skills:

```bash
dimonta skills list
```

Execute a skill (parameters can be passed as `key=value` pairs):

```bash
dimonta skills exec DetectScrews -p image_path=img.png
```

Inspect the small in-memory database:

```bash
dimonta db show
```

## Demo Ideas

- **Full Screw Workflow** – Run a sequence of skills to detect screws,
  refine the position of one screw and remove it:

  ```bash
  dimonta skills exec DetectScrews -p image_path=img.png
  dimonta skills exec DismantlingPlanner
  dimonta skills exec LocateScrew -p screw_id=S1
  dimonta skills exec Unscrew -p target_id=S1 -p torque=5
  ```

- **Generate Skill Documentation** – Recreate the markdown overview of
  available skills:

  ```bash
  skill-docs > docs/skills.md
  ```

These examples are a starting point for experimenting with new skills or
building larger robotic workflows on top of the framework.
