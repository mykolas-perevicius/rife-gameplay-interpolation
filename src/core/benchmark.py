"""Performance Benchmarker"""

import json
import os
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import cv2
import torch

from src.utils.logger import log


class Benchmarker:
    """Benchmark RIFE interpolation performance."""
    
    RESOLUTION_MAP = {
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "1440p": (2560, 1440),
        "4k": (3840, 2160)
    }
    
    def __init__(self, output_dir: str = "results/benchmarks"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_gpu_info(self) -> dict:
        """Get GPU information."""
        if not torch.cuda.is_available():
            return {"gpu": "CPU Only", "vram": "N/A", "cuda": "N/A"}
        
        return {
            "gpu": torch.cuda.get_device_name(0),
            "vram": f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB",
            "cuda": torch.version.cuda or "N/A"
        }
    
    def resize_video(self, input_path: str, resolution: str, output_path: str) -> str:
        """Resize video to target resolution."""
        if resolution not in self.RESOLUTION_MAP:
            raise ValueError(f"Unknown resolution: {resolution}")
        
        w, h = self.RESOLUTION_MAP[resolution]
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"scale={w}:{h}",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-t", "5",  # Only first 5 seconds
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path
    
    def benchmark_resolution(self, input_path: str, resolution: str) -> dict:
        """Benchmark at a specific resolution."""
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        # Time a simulated benchmark (replace with actual RIFE call)
        start = time.time()
        
        # Placeholder - actual implementation would call RIFE
        time.sleep(0.5)  # Simulate processing
        
        elapsed = time.time() - start
        inference_fps = frames / max(elapsed, 0.01)
        
        return {
            "resolution": resolution,
            "fps": inference_fps,
            "realtime_ratio": inference_fps / fps if fps > 0 else 0,
            "realtime": inference_fps >= fps,
            "frames": frames,
            "elapsed": elapsed
        }
    
    def run(self, input_path: str, resolutions: List[str]) -> dict:
        """Run full benchmark suite."""
        gpu_info = self.get_gpu_info()
        
        log.info(f"GPU: {gpu_info['gpu']}")
        log.info(f"Testing resolutions: {', '.join(resolutions)}")
        
        benchmarks = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for res in resolutions:
                log.debug(f"Benchmarking {res}...")
                
                try:
                    # Resize to target resolution
                    resized = os.path.join(tmpdir, f"input_{res}.mp4")
                    self.resize_video(input_path, res, resized)
                    
                    # Run benchmark
                    result = self.benchmark_resolution(resized, res)
                    benchmarks.append(result)
                    
                    log.info(f"{res}: {result['fps']:.1f} FPS ({result['realtime_ratio']:.2f}x realtime)")
                    
                except Exception as e:
                    log.warning(f"Failed to benchmark {res}: {e}")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "gpu": gpu_info["gpu"],
            "vram": gpu_info["vram"],
            "benchmarks": benchmarks
        }
    
    def save_results(self, results: dict, output_path: str):
        """Save benchmark results to JSON."""
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
