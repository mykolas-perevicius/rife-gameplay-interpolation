<div align="center">

# 🎮 RIFE Gameplay Interpolation

**AI-Powered Frame Enhancement for Gaming Videos**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CS 474](https://img.shields.io/badge/NJIT-CS%20474-red.svg)](https://njit.edu)

*Convert 30 FPS gameplay recordings to buttery-smooth 60+ FPS using deep learning*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Research](#research) • [Results](#results)

---

</div>

## 🎯 Overview

This project uses **RIFE (Real-Time Intermediate Flow Estimation)** to enhance recorded gameplay footage through AI-powered frame interpolation. Instead of traditional frame blending, RIFE uses deep neural networks to estimate optical flow and synthesize realistic intermediate frames.
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  30 FPS Input   │ ──► │   RIFE v4.25    │ ──► │  60 FPS Output  │
│  Tarkov.mp4     │     │   Neural Net    │     │  Smooth motion  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## ✨ Features

- **🚀 Fast Processing** - GPU-accelerated inference on RTX 3090
- **📊 Quality Metrics** - PSNR, SSIM, VMAF evaluation
- **🎨 Beautiful CLI** - Rich terminal interface with progress bars
- **📈 Benchmarking** - Performance testing across resolutions
- **🔧 Easy Setup** - One-command environment configuration
- **📝 Logging** - Comprehensive logs for debugging and analysis

## 🛠️ Installation

### Prerequisites

- **GPU**: NVIDIA GPU with CUDA support (tested on RTX 3090)
- **Python**: 3.10 or higher
- **FFmpeg**: Installed and in PATH

### Quick Start
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/rife-gameplay-interpolation.git
cd rife-gameplay-interpolation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Setup RIFE (downloads models)
python -m src.cli setup

# Verify installation
python -m src.cli info
```

## 📖 Usage

### CLI Commands
```bash
# Show help
rife --help

# Interpolate video (2x frame rate)
rife interpolate gameplay.mp4 gameplay_60fps.mp4

# Interpolate with 4x multiplier
rife interpolate input.mp4 output.mp4 --multi 4

# Calculate quality metrics
rife metrics interpolated.mp4 ground_truth.mp4

# Run performance benchmark
rife benchmark gameplay.mp4

# Create synthetic test data (downsample 60fps to 30fps)
rife downsample recording_60fps.mp4 recording_30fps.mp4 --skip 2

# Show system info
rife info
```

### Python API
```python
from src.core.interpolator import RIFEInterpolator
from src.core.metrics import MetricsCalculator

# Interpolate video
interpolator = RIFEInterpolator(model_version="4.25")
stats = interpolator.process("input.mp4", "output.mp4", multi=2)
print(f"Processed at {stats['processing_fps']:.1f} FPS")

# Calculate metrics
calc = MetricsCalculator()
results = calc.calculate("output.mp4", "reference.mp4")
print(f"PSNR: {results['psnr']:.2f} dB")
```

### Using Make
```bash
make help          # Show available commands
make install       # Install dependencies
make setup         # Download models
make test          # Run tests
make lint          # Run linting
make format        # Format code
```

## 🔬 Research

### Problem Statement

High frame-rate video enhances gaming experiences, but recording at 120+ FPS requires significant resources. AI frame interpolation offers a post-processing solution to convert 30 FPS recordings to 60+ FPS with minimal artifacts.

### Research Questions

1. **Quality**: How close can AI interpolation match native high FPS footage?
2. **Artifacts**: Where does interpolation fail? (particles, HUD, fast motion)
3. **Performance**: Is this practical for content creation workflows?

### Methodology

1. **Dataset Creation**: Record gameplay at native 60 FPS (ground truth)
2. **Synthetic Input**: Extract every other frame to create 30 FPS test data
3. **Interpolation**: Process through RIFE to generate 60 FPS output
4. **Evaluation**: Compare against ground truth using PSNR, SSIM, VMAF

### Course Connections (CS 474)

| Course Topic | Project Connection |
|--------------|-------------------|
| **Week 4: Autoencoders** | RIFE's learned feature pyramids for multi-scale motion |
| **Week 6: Diffusion Models** | Gram matrix loss (from FILM) for texture preservation |
| **Week 11: World Models** | Temporal motion estimation as scene understanding |

## 📊 Results

*Results will be populated after experiments*

| Game | Resolution | PSNR (dB) | SSIM | VMAF | Inference FPS |
|------|------------|-----------|------|------|---------------|
| Escape from Tarkov | 1080p | -- | -- | -- | -- |
| ARC Raiders | 1080p | -- | -- | -- | -- |

### Artifact Analysis

| Type | Description | Frequency |
|------|-------------|-----------|
| **Ghosting** | Semi-transparent trails on fast objects | -- |
| **Tearing** | HUD elements split incorrectly | -- |
| **Blur** | Excessive smoothing on edges | -- |

## 📁 Project Structure
```
rife-gameplay-interpolation/
├── src/
│   ├── cli.py              # Beautiful CLI interface
│   ├── core/
│   │   ├── interpolator.py # RIFE wrapper
│   │   ├── metrics.py      # Quality metrics
│   │   ├── benchmark.py    # Performance testing
│   │   └── extractor.py    # Frame utilities
│   └── utils/
│       ├── logger.py       # Logging setup
│       ├── config.py       # Configuration
│       └── setup.py        # Environment setup
├── configs/
│   └── default.yaml        # Default settings
├── data/                   # Video files (gitignored)
├── results/                # Metrics & benchmarks
├── logs/                   # Application logs
├── Makefile               # Convenience commands
└── requirements.txt       # Dependencies
```

## 📚 References

1. Huang, Z. et al. **"RIFE: Real-Time Intermediate Flow Estimation for Video Frame Interpolation."** ECCV 2022. [arXiv:2011.06294](https://arxiv.org/abs/2011.06294)

2. Reda, F. et al. **"FILM: Frame Interpolation for Large Motion."** ECCV 2022. [arXiv:2202.04901](https://arxiv.org/abs/2202.04901)

3. [Practical-RIFE](https://github.com/hzwer/Practical-RIFE) - Production-ready implementation

4. [MSU VFI Benchmark](https://videoprocessing.ai/benchmarks/video-frame-interpolation.html) - Quality evaluation

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Dr. Amy K. Hoover** - CS 474 Course Instruction, NJIT
- **hzwer** - Practical-RIFE implementation
- **Google Research** - FILM architecture insights

---

<div align="center">

**CS 474: Introduction to Generative AI** • Fall 2025 • NJIT

*Made with ❤️ and lots of GPU cycles*

</div>
