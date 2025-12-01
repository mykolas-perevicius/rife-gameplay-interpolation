# AI-Powered Frame Interpolation for Gameplay Video Enhancement

> CS 474: Introduction to Generative AI — Fall 2025 Final Project  
> **Author:** Mykolas Perevicius | **Instructor:** Dr. Amy K. Hoover, NJIT

## Overview

Using **RIFE (Real-Time Intermediate Flow Estimation)** to convert 30 FPS gameplay recordings to 60+ FPS, evaluating interpolation quality with PSNR/SSIM/VMAF metrics.
```
30 FPS Gameplay ──► RIFE v4.25 ──► 60 FPS Output
```

## Quick Start
```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/download_models.py

# Run interpolation
python src/interpolate.py -i input.mp4 -o output.mp4 --multi 2

# Calculate metrics
python src/metrics.py -i output.mp4 -r ground_truth.mp4
```

## Research Questions

1. **Quality:** How close can AI interpolation get to native 60 FPS?
2. **Artifacts:** Where does it fail? (particles, HUD, fast motion)
3. **Performance:** Practical for content creators?

## Project Structure
```
├── src/                 # Core pipeline scripts
├── scripts/             # Setup utilities  
├── configs/             # Configuration files
├── data/                # Video files (gitignored)
├── results/             # Metrics and benchmarks
└── docs/                # Presentation materials
```

## References

1. Huang et al. "RIFE: Real-Time Intermediate Flow Estimation" ECCV 2022
2. Reda et al. "FILM: Frame Interpolation for Large Motion" ECCV 2022
3. [Practical-RIFE](https://github.com/hzwer/Practical-RIFE)
