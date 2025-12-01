#!/usr/bin/env python3
"""
Comprehensive experiment runner for RIFE gameplay interpolation project.
Handles the full pipeline from video preprocessing to metrics calculation.
"""

import os
import sys
import json
import csv
import subprocess
import time
import random
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
import torch
import skvideo.io
from skvideo.measure import psnr, ssim

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class ExperimentRunner:
    def __init__(self, source_video: str, clip_duration: int = 10, scale: float = 0.5):
        self.source_video = Path(source_video)
        self.clip_duration = clip_duration
        self.scale = scale

        # Setup paths
        self.data_dir = PROJECT_ROOT / "data"
        self.input_dir = self.data_dir / "input"
        self.output_dir = self.data_dir / "output"
        self.results_dir = PROJECT_ROOT / "results"
        self.metrics_dir = self.results_dir / "metrics"
        self.rife_dir = PROJECT_ROOT / "Practical-RIFE"

        # Create directories
        for d in [self.input_dir, self.output_dir, self.metrics_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # File paths
        self.clip_60fps = self.input_dir / "arc_clip_60fps.mp4"
        self.clip_30fps = self.input_dir / "arc_clip_30fps.mp4"
        self.interpolated_60fps = self.output_dir / "arc_interpolated_60fps.mp4"
        self.comparison_side_by_side = self.output_dir / "comparison_sidebyside.mp4"
        self.blind_test = self.output_dir / "blind_test.mp4"

    def log(self, message: str):
        """Print timestamped log message."""
        print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def run_command(self, cmd: List[str], description: str) -> bool:
        """Run a shell command and return success status."""
        self.log(f"{description}...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Error: {e.stderr}")
            return False

    def extract_clip(self) -> bool:
        """Extract 10-second clip from source video at 60fps."""
        self.log("Step 1: Extracting 10-second clip from source video")

        if self.clip_60fps.exists():
            self.log(f"Clip already exists at {self.clip_60fps}")
            return True

        cmd = [
            "ffmpeg", "-y",
            "-i", str(self.source_video),
            "-t", str(self.clip_duration),
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-an",  # No audio for simplicity
            str(self.clip_60fps)
        ]

        return self.run_command(cmd, "Extracting clip")

    def downsample_to_30fps(self) -> bool:
        """Downsample 60fps clip to 30fps by selecting every other frame."""
        self.log("Step 2: Downsampling to 30fps")

        if self.clip_30fps.exists():
            self.log(f"30fps clip already exists at {self.clip_30fps}")
            return True

        # Read video and extract every other frame
        cap = cv2.VideoCapture(str(self.clip_60fps))
        if not cap.isOpened():
            self.log(f"Error: Could not open {self.clip_60fps}")
            return False

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.log(f"Source: {width}x{height} @ {fps}fps")

        # Use ffmpeg to downsample
        cmd = [
            "ffmpeg", "-y",
            "-i", str(self.clip_60fps),
            "-vf", "select='not(mod(n\\,2))',setpts=N/FRAME_RATE/TB",
            "-r", "30",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            str(self.clip_30fps)
        ]

        cap.release()
        return self.run_command(cmd, "Downsampling to 30fps")

    def interpolate_with_rife(self) -> Tuple[bool, Dict]:
        """Run RIFE interpolation to convert 30fps back to 60fps."""
        self.log("Step 3: Running RIFE interpolation")

        start_time = time.time()

        cmd = [
            "python3",
            str(self.rife_dir / "inference_video.py"),
            "--video", str(self.clip_30fps),
            "--output", str(self.interpolated_60fps),
            "--model", str(PROJECT_ROOT / "train_log"),
            "--scale", str(self.scale),
            "--multi", "2",
            "--fp16"
        ]

        os.chdir(self.rife_dir)
        success = self.run_command(cmd, "Running RIFE")
        os.chdir(PROJECT_ROOT)

        elapsed_time = time.time() - start_time

        # Get frame count to calculate processing FPS
        if success and self.interpolated_60fps.exists():
            cap = cv2.VideoCapture(str(self.interpolated_60fps))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

            processing_fps = frame_count / elapsed_time if elapsed_time > 0 else 0

            stats = {
                "elapsed_time": elapsed_time,
                "frame_count": frame_count,
                "processing_fps": processing_fps
            }

            self.log(f"Processed {frame_count} frames in {elapsed_time:.2f}s ({processing_fps:.2f} FPS)")
            return True, stats

        return False, {}

    def calculate_metrics(self) -> Dict:
        """Calculate PSNR and SSIM between interpolated and original 60fps."""
        self.log("Step 4: Calculating quality metrics (PSNR/SSIM)")

        # Load videos
        self.log("Loading reference video...")
        ref_video = skvideo.io.vread(str(self.clip_60fps), as_grey=True)

        self.log("Loading interpolated video...")
        interp_video = skvideo.io.vread(str(self.interpolated_60fps), as_grey=True)

        # Ensure same length
        min_frames = min(len(ref_video), len(interp_video))
        ref_video = ref_video[:min_frames]
        interp_video = interp_video[:min_frames]

        self.log(f"Comparing {min_frames} frames...")

        # Calculate PSNR
        self.log("Calculating PSNR...")
        psnr_scores = psnr(ref_video, interp_video)
        psnr_mean = float(np.mean(psnr_scores))
        psnr_std = float(np.std(psnr_scores))

        # Calculate SSIM
        self.log("Calculating SSIM...")
        ssim_scores = ssim(ref_video, interp_video)
        ssim_mean = float(np.mean(ssim_scores))
        ssim_std = float(np.std(ssim_scores))

        metrics = {
            "psnr_mean": psnr_mean,
            "psnr_std": psnr_std,
            "ssim_mean": ssim_mean,
            "ssim_std": ssim_std,
            "frame_count": min_frames
        }

        self.log(f"PSNR: {psnr_mean:.2f} ± {psnr_std:.2f} dB")
        self.log(f"SSIM: {ssim_mean:.4f} ± {ssim_std:.4f}")

        return metrics

    def save_metrics(self, metrics: Dict, processing_stats: Dict):
        """Save metrics to JSON and CSV files."""
        self.log("Step 5: Saving metrics")

        combined = {**metrics, **processing_stats}
        combined["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        combined["source_video"] = str(self.source_video)
        combined["scale"] = self.scale

        # Save JSON
        json_path = self.metrics_dir / "arc_raiders_metrics.json"
        with open(json_path, "w") as f:
            json.dump(combined, f, indent=2)
        self.log(f"Saved JSON to {json_path}")

        # Save CSV
        csv_path = self.metrics_dir / "arc_raiders_metrics.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=combined.keys())
            writer.writeheader()
            writer.writerow(combined)
        self.log(f"Saved CSV to {csv_path}")

    def create_side_by_side_comparison(self) -> bool:
        """Create side-by-side comparison video."""
        self.log("Step 6: Creating side-by-side comparison")

        cmd = [
            "ffmpeg", "-y",
            "-i", str(self.clip_60fps),
            "-i", str(self.interpolated_60fps),
            "-filter_complex",
            "[0:v][1:v]hstack=inputs=2[v];" +
            "[v]drawtext=text='Original 60fps':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5," +
            "drawtext=text='RIFE Interpolated':x=w/2+10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[vout]",
            "-map", "[vout]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            str(self.comparison_side_by_side)
        ]

        return self.run_command(cmd, "Creating side-by-side comparison")

    def create_blind_test(self) -> bool:
        """Create A/B blind test video with random ordering."""
        self.log("Step 7: Creating A/B blind test")

        # Randomly decide order
        is_original_first = random.choice([True, False])
        first_label = "A" if is_original_first else "B"
        second_label = "B" if is_original_first else "A"
        first_video = str(self.clip_60fps) if is_original_first else str(self.interpolated_60fps)
        second_video = str(self.interpolated_60fps) if is_original_first else str(self.clip_60fps)

        # Create metadata file with answer
        answer_file = self.output_dir / "blind_test_answer.txt"
        with open(answer_file, "w") as f:
            f.write(f"Clip A: {'Original' if is_original_first else 'Interpolated'}\n")
            f.write(f"Clip B: {'Interpolated' if is_original_first else 'Original'}\n")

        # Concatenate videos with labels
        cmd = [
            "ffmpeg", "-y",
            "-i", first_video,
            "-i", second_video,
            "-filter_complex",
            f"[0:v]drawtext=text='Clip {first_label}':x=10:y=10:fontsize=72:fontcolor=yellow:box=1:boxcolor=black@0.5[v0];" +
            f"[1:v]drawtext=text='Clip {second_label}':x=10:y=10:fontsize=72:fontcolor=yellow:box=1:boxcolor=black@0.5[v1];" +
            "[v0][v1]concat=n=2:v=1:a=0[vout]",
            "-map", "[vout]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            str(self.blind_test)
        ]

        success = self.run_command(cmd, "Creating blind test")
        if success:
            self.log(f"Answer saved to {answer_file}")
        return success

    def run_full_experiment(self) -> bool:
        """Run the complete experiment pipeline."""
        self.log("="*60)
        self.log("Starting RIFE Gameplay Interpolation Experiment")
        self.log("="*60)

        # Step 1: Extract clip
        if not self.extract_clip():
            return False

        # Step 2: Downsample to 30fps
        if not self.downsample_to_30fps():
            return False

        # Step 3: Interpolate with RIFE
        success, processing_stats = self.interpolate_with_rife()
        if not success:
            return False

        # Step 4: Calculate metrics
        metrics = self.calculate_metrics()

        # Step 5: Save metrics
        self.save_metrics(metrics, processing_stats)

        # Step 6: Create side-by-side comparison
        self.create_side_by_side_comparison()

        # Step 7: Create blind test
        self.create_blind_test()

        self.log("="*60)
        self.log("Experiment completed successfully!")
        self.log("="*60)

        return True

def main():
    source_video = "/mnt/c/Users/miciu/Videos/ARC Raiders - 2025-11-13 3-29-45 AM.mp4"

    if not Path(source_video).exists():
        print(f"Error: Source video not found at {source_video}")
        return 1

    runner = ExperimentRunner(source_video, clip_duration=10, scale=0.5)

    if runner.run_full_experiment():
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
