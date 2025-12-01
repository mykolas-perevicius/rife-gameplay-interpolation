"""Frame Extraction Utilities"""

import subprocess
from pathlib import Path

import cv2

from src.utils.logger import log


class FrameExtractor:
    """Extract and manipulate video frames."""
    
    def downsample(self, input_path: str, output_path: str, skip: int = 2) -> dict:
        """
        Create downsampled video by keeping every Nth frame.
        
        Args:
            input_path: Source video
            output_path: Output video
            skip: Keep every Nth frame
        
        Returns:
            dict with statistics
        """
        # Get input info
        cap = cv2.VideoCapture(input_path)
        input_fps = cap.get(cv2.CAP_PROP_FPS)
        input_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        # Use FFmpeg select filter
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"select='not(mod(n,{skip}))',setpts=N/FRAME_RATE/TB",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-an",
            output_path
        ]
        
        log.debug(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
        
        # Get output info
        cap = cv2.VideoCapture(output_path)
        output_fps = cap.get(cv2.CAP_PROP_FPS)
        output_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        return {
            "input_fps": input_fps,
            "output_fps": output_fps,
            "input_frames": input_frames,
            "output_frames": output_frames,
            "skip": skip
        }
