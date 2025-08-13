# RealSense Setup

The `CaptureRealSenseImage` skill can acquire a frame from an Intel RealSense camera.
To use a physical camera:

1. Install the `pyrealsense2` drivers and ensure the device is connected via USB.
2. Execute the skill with the parameter `use_camera=true`:
   ```bash
   dimonta skills exec CaptureRealSenseImage -p use_camera=true
   ```
3. The captured image is stored in the database under the key `camera_image`.

If no camera is available, omit the parameter or set `use_camera=false`.
A small dummy image will be written to the database so dependent skills can still run.
