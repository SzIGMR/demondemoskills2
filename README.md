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

### Configuration

Configuration values for the runtime, database and individual skills are stored
in ``config.json`` (created on first write).  To edit the configuration in a
browser run the built-in web UI:

```bash
dimonta web config --port 8000
```

Open ``http://localhost:8000`` in your browser and adjust the JSON as needed.

### YOLO Result Viewer

After running detection skills you can inspect the stored image and screw
positions in a simple browser-based UI:

```bash
dimonta web results --port 8001
```

Open ``http://localhost:8001`` to view the image with annotated detections and
their coordinates.

### Headless Server

Run the FastAPI based server to execute skills via HTTP, WebSocket or XML:

```bash
uvicorn di_core.server:app --reload
```

`GET /skills` lists all registered skills. To run a skill send a JSON payload
to `POST /execute` or connect to the WebSocket endpoint at
`ws://localhost:8000/ws/execute`. A minimal HTML client is available at
`web/index.html`.

## Demo Ideas

- **Manual Full Screw Workflow** – Run a sequence of skills to detect screws,
  refine the position of one screw and remove it:

  ```bash
  dimonta skills exec DetectScrews -p image_path=img.png
  dimonta skills exec DismantlingPlanner
  dimonta skills exec LocateScrew -p screw_id=S1
  dimonta skills exec Unscrew -p target_id=S1 -p torque=5

  ```

- **Automated Full Screw Removal** - run the full sequence based on an image handeled by a behaviour tree;

  ```bash
  dimonta skills exec ScrewRemovalWorkflow -p image_path=img.png
  ```

- **Generate Skill Documentation** – Recreate the markdown overview of
  available skills:

  ```bash
  skill-docs > docs/skills.md
  ```

  The command prints the markdown to `stdout`, so you may also supply a
  destination path directly:

  ```bash
  skill-docs docs/skills.md
  ```

These examples are a starting point for experimenting with new skills or
building larger robotic workflows on top of the framework.

## Additional Hardware/Model Setup

- [RealSense camera instructions](docs/realsense.md)
- [YOLO model instructions](docs/yolo.md)
