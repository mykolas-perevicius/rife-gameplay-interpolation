#!/usr/bin/env python3
"""Calculate PSNR/SSIM metrics and create comparison videos."""

import json
import csv
import sys
import time
import random
import subprocess
from pathlib import Path
from typing import Dict

import numpy as np
import cv2
import skvideo.io
from skvideo.measure import psnr, ssim

PROJECT_ROOT = Path(__file__).parent.parent

def log(message: str):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def calculate_metrics(ref_path: str, interp_path: str) -> Dict:
    """Calculate PSNR and SSIM metrics."""
    log("Calculating quality metrics (PSNR/SSIM)")

    # Load videos as grayscale
    log(f"Loading reference video: {ref_path}")
    ref_video = skvideo.io.vread(ref_path, as_grey=True)

    log(f"Loading interpolated video: {interp_path}")
    interp_video = skvideo.io.vread(interp_path, as_grey=True)

    # Ensure same length
    min_frames = min(len(ref_video), len(interp_video))
    ref_video = ref_video[:min_frames]
    interp_video = interp_video[:min_frames]

    log(f"Comparing {min_frames} frames...")

    # Calculate PSNR
    log("Calculating PSNR...")
    psnr_scores = psnr(ref_video, interp_video)
    psnr_mean = float(np.mean(psnr_scores))
    psnr_std = float(np.std(psnr_scores))

    # Calculate SSIM
    log("Calculating SSIM...")
    ssim_scores = ssim(ref_video, interp_video)
    ssim_mean = float(np.mean(ssim_scores))
    ssim_std = float(np.std(ssim_scores))

    metrics = {
        "psnr_mean": psnr_mean,
        "psnr_std": psnr_std,
        "psnr_min": float(np.min(psnr_scores)),
        "psnr_max": float(np.max(psnr_scores)),
        "ssim_mean": ssim_mean,
        "ssim_std": ssim_std,
        "ssim_min": float(np.min(ssim_scores)),
        "ssim_max": float(np.max(ssim_scores)),
        "frame_count": min_frames
    }

    log(f"PSNR: {psnr_mean:.2f} ± {psnr_std:.2f} dB (range: {metrics['psnr_min']:.2f}-{metrics['psnr_max']:.2f})")
    log(f"SSIM: {ssim_mean:.4f} ± {ssim_std:.4f} (range: {metrics['ssim_min']:.4f}-{metrics['ssim_max']:.4f})")

    return metrics

def get_video_info(video_path: str) -> Dict:
    """Get video metadata."""
    cap = cv2.VideoCapture(video_path)
    info = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    }
    cap.release()
    return info

def save_metrics(metrics: Dict, output_dir: Path):
    """Save metrics to JSON and CSV."""
    log("Saving metrics")

    # Add timestamp
    metrics["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # Save JSON
    json_path = output_dir / "arc_raiders_metrics.json"
    with open(json_path, "w") as f:
        json.dump(metrics, f, indent=2)
    log(f"Saved JSON to {json_path}")

    # Save CSV
    csv_path = output_dir / "arc_raiders_metrics.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        writer.writeheader()
        writer.writerow(metrics)
    log(f"Saved CSV to {csv_path}")

def create_side_by_side(ref_path: str, interp_path: str, output_path: str) -> bool:
    """Create side-by-side comparison video."""
    log("Creating side-by-side comparison")

    cmd = [
        "ffmpeg", "-y",
        "-i", ref_path,
        "-i", interp_path,
        "-filter_complex",
        "[0:v][1:v]hstack=inputs=2[v];" +
        "[v]drawtext=text='Original 60fps':x=10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5," +
        "drawtext=text='RIFE Interpolated':x=w/2+10:y=10:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5[vout]",
        "-map", "[vout]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-t", "10",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        log(f"Created {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error: {e.stderr.decode()}")
        return False

def create_blind_test(ref_path: str, interp_path: str, output_path: str, answer_path: str) -> bool:
    """Create A/B blind test video."""
    log("Creating A/B blind test")

    # Randomly decide order
    is_original_first = random.choice([True, False])
    first_label = "A"
    second_label = "B"
    first_video = ref_path if is_original_first else interp_path
    second_video = interp_path if is_original_first else ref_path

    # Save answer
    with open(answer_path, "w") as f:
        f.write(f"Clip A: {'Original 60fps' if is_original_first else 'RIFE Interpolated'}\n")
        f.write(f"Clip B: {'RIFE Interpolated' if is_original_first else 'Original 60fps'}\n")
        f.write(f"\nGuess which clip is the AI-interpolated one!\n")

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
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        log(f"Created {output_path}")
        log(f"Answer saved to {answer_path}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error: {e.stderr.decode()}")
        return False

def main():
    # Paths
    input_dir = PROJECT_ROOT / "data" / "input"
    output_dir = PROJECT_ROOT / "data" / "output"
    metrics_dir = PROJECT_ROOT / "results" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    ref_video = str(input_dir / "arc_clip_60fps.mp4")
    interp_video = str(output_dir / "arc_interpolated_60fps.mp4")

    log("="*60)
    log("Calculating Metrics and Creating Comparison Videos")
    log("="*60)

    # Get video info
    log("Video Information:")
    ref_info = get_video_info(ref_video)
    log(f"Reference: {ref_info['width']}x{ref_info['height']} @ {ref_info['fps']:.2f}fps, {ref_info['frame_count']} frames")

    interp_info = get_video_info(interp_video)
    log(f"Interpolated: {interp_info['width']}x{interp_info['height']} @ {interp_info['fps']:.2f}fps, {interp_info['frame_count']} frames")

    # Calculate metrics
    metrics = calculate_metrics(ref_video, interp_video)

    # Add video info to metrics
    metrics["reference_resolution"] = f"{ref_info['width']}x{ref_info['height']}"
    metrics["reference_fps"] = ref_info['fps']
    metrics["interpolated_resolution"] = f"{interp_info['width']}x{interp_info['height']}"
    metrics["interpolated_fps"] = interp_info['fps']

    # Estimate processing speed (based on RIFE output - ~23 FPS average)
    estimated_processing_fps = 22.5  # From the progress bar output
    metrics["estimated_processing_fps"] = estimated_processing_fps

    # Save metrics
    save_metrics(metrics, metrics_dir)

    # Create comparison videos
    comparison_path = str(output_dir / "comparison_sidebyside.mp4")
    create_side_by_side(ref_video, interp_video, comparison_path)

    blind_test_path = str(output_dir / "blind_test.mp4")
    answer_path = str(output_dir / "blind_test_answer.txt")
    create_blind_test(ref_video, interp_video, blind_test_path, answer_path)

    log("="*60)
    log("Processing Complete!")
    log("="*60)

    return 0

if __name__ == "__main__":
    sys.exit(main())
