# Skill Documentation

## CaptureRealSenseImage (v1.2.0)
Capture an image from an Intel RealSense camera and store it in the database.

**Inputs**
- `use_camera`: Set to `true` to read from a RealSense camera, otherwise a sample PNG is stored
- `sample_dir`: Directory containing PNG images to use when the camera is unavailable

**Outputs**
- `image_key`: Database key where the image is stored

## DetectScrews (v1.2.0)
Detect screws in an image and store their positions.

**Inputs**
- `image_path`: Path to the camera image (optional if image is stored in db)
- `model_path`: Optional path to a YOLOv8 model
- `use_model`: Set to `true` to run a YOLOv8 model, otherwise a simulated detection is returned

**Outputs**
- `screw_ids`: Comma separated screw identifiers

## DismantlingPlanner (v1.0.0)
Plan a random sequence of screws to dismantle.

**Outputs**
- `plan`: Comma separated screw identifiers

## LocateScrew (v1.0.0)
Move to a screw and refine its position via camera.

**Inputs**
- `screw_id`: Identifier of the screw to localize

**Outputs**
- `x`: Refined x position
- `y`: Refined y position

## ScrewRemovalWorkflow (v1.0.0)
Run detection, planning and removal of all screws using a behavior tree.

**Inputs**
- `image_path`: Path to the camera image
- `torque`: Torque in Nm

**Outputs**
- `removed_ids`: Comma separated removed screw identifiers

## Unscrew (v1.0.0)
Remove a screw using a preset torque.

**Inputs**
- `target_id`: ID of the screw to remove
- `torque`: Torque in Nm

**Outputs**
- `removed`: true if screw removed
- `time_s`: time taken in seconds
