# Skill Documentation

## DetectScrews (v1.0.0)
Detect screws in an image and store their positions.

**Inputs**
- `image_path`: Path to the camera image

**Outputs**
- `screw_ids`: Comma separated screw identifiers

## LocateScrew (v1.0.0)
Move to a screw and refine its position via camera.

**Inputs**
- `screw_id`: Identifier of the screw to localize

**Outputs**
- `x`: Refined x position
- `y`: Refined y position

## Unscrew (v1.0.0)
Remove a screw using a preset torque.

**Inputs**
- `target_id`: ID of the screw to remove
- `torque`: Torque in Nm

**Outputs**
- `removed`: true if screw removed
- `time_s`: time taken in seconds
