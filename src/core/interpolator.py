"""RIFE Frame Interpolator"""

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Optional

import cv2
from loguru import logger

from src.utils.logger import log


class RIFEInterpolator:
    """Wrapper for Practical-RIFE inference."""
    
    RIFE_PATH = Path("Practical-RIFE")
    
    def __init__(self, model_version: str = "4.25"):
        self.model_version = model_version
        self._validate_setup()
    
    def _validate_setup(self):
        """Check that RIFE is properly installed."""
        if not self.RIFE_PATH.exists():
            raise RuntimeError(
                f"Practical-RIFE not found at {self.RIFE_PATH}. "
                "Run: rife setup"
            )
        
        model_path = Path("train_log/flownet.pkl")
        if not model_path.exists():
            raise RuntimeError(
                f"Model weights not found. Run: rife setup"
            )
    
    def get_video_info(self, path: str) -> dict:
        """Extract video metadata."""
        cap = cv2.VideoCapture(path)
        info = {
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(cap.get(cv2.CAP_PROP_FPS), 1)
        }
        cap.release()
        return info
    
    def process(
        self,
        input_path: str,
        output_path: str,
        multi: int = 2,
        scale: float = 1.0,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> dict:
        """
        Run RIFE interpolation.
        
        Args:
            input_path: Input video path
            output_path: Output video path
            multi: Frame multiplication factor
            scale: Input scale factor
            progress_callback: Optional callback for progress updates
        
        Returns:
            dict with processing statistics
        """
        input_info = self.get_video_info(input_path)
        
        log.info(f"Input: {input_info['width']}x{input_info['height']} @ {input_info['fps']:.1f} FPS")
        log.info(f"Target: {input_info['fps'] * multi:.1f} FPS ({multi}x)")
        
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        # Build command
        cmd = [
            sys.executable,
            str(self.RIFE_PATH / "inference_video.py"),
            f"--multi={multi}",
            f"--video={input_path}",
            f"--output={output_path}",
        ]
        
        if scale != 1.0:
            cmd.append(f"--scale={scale}")
        
        log.debug(f"Running: {' '.join(cmd)}")
        
        # Execute with progress tracking
        start_time = time.time()
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Parse output for progress
        for line in process.stdout:
            log.debug(line.strip())
            # Try to extract progress percentage
            if "%" in line and progress_callback:
                try:
                    pct = float(line.split("%")[0].split()[-1])
                    progress_callback(pct)
                except:
                    pass
        
        process.wait()
        elapsed = time.time() - start_time
        
        if process.returncode != 0:
            raise RuntimeError(f"RIFE process failed with code {process.returncode}")
        
        # Get output info
        output_info = self.get_video_info(output_path)
        
        return {
            "input_fps": input_info["fps"],
            "output_fps": output_info["fps"],
            "input_frames": input_info["frames"],
            "output_frames": output_info["frames"],
            "elapsed": elapsed,
            "processing_fps": input_info["frames"] / elapsed if elapsed > 0 else 0,
            "multi": multi,
            "resolution": f"{input_info['width']}x{input_info['height']}"
        }
