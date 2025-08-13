# YOLO Model Setup

The `DetectScrews` skill can run a YOLOv8 model to locate screws in an image.

To use a real model:

1. Install the `ultralytics` package and download a YOLOv8 weight file (e.g. `yolov8n.pt`).
2. Execute the skill with `use_model=true` and optionally provide a custom `model_path`:
   ```bash
   dimonta skills exec DetectScrews -p use_model=true -p model_path=/path/to/model.pt
   ```
3. Detected screw positions are stored in the database under the key `screws`.

If a model is not available, omit the parameter or set `use_model=false`.
The skill will return a simulated detection so that workflows can continue.
