Simple FFmpeg binding for python, mainly created for personal use.

## Installation using pip
```bash
pip install ffmpeg-py
```

Example:
```python
from FFmpeg.ffmpeg import FFmpeg
import subprocess

ffmpeg = FFmpeg()
ff = (
    ffmpeg
    .OverwriteOutput()
    .addInput("video1.webm")
    .addInput("./logo.png")
    .addInput("video2.webm")
    .videoCodec("libx264")
    .audioCodec("aac")
    .videoFramerate(30)
    .videoResolution(resString="1920x1080")
    .scale2refFilter(2, 0, "oh*mdar:ih*0.2", "camera", "video")  # resize camera to 20% of screen height
    .overlayFilter("video", "1", "W-w-10", "H-h-10", "v")  # overlay logo on bottom right
    .overlayFilter("v", "camera", "10", "10")  # overlay camera on top left
    .output("output.mp4")  # output file
)
code, stdout, stderr = ff.execute(stderr=subprocess.STDOUT, shell=False)
print(code, stdout, stderr)
```

## INFO

- FFmpeg.ffmpeg.FFmpeg() - Main class, contains logic for executing command using subprocess
- FFmpeg.ffmpegCommandBuilder.FFmpegCommandBuilder() - Class for building ffmpeg command, contains all methods for ffmpeg filters, codecs and other options


