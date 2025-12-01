# Usage Guide

## Quick Start

After installation, the `rife` command provides access to all functionality.

### Check System

Verify your GPU and dependencies:
```bash
python -m src.cli info
```

### Setup Environment

Download RIFE models and clone Practical-RIFE:
```bash
python -m src.cli setup
```

## Commands

### Interpolate Video

Basic 2x interpolation (30 FPS → 60 FPS):
```bash
python -m src.cli interpolate input.mp4 output.mp4
```

With options:
```bash
python -m src.cli interpolate input.mp4 output.mp4 \
    --multi 4 \
    --model 4.25 \
    --scale 0.5
```

Options:
- `--multi`: Frame multiplier (2, 4, or 8)
- `--model`: RIFE model version
- `--scale`: Input scale factor (0.5 = half resolution, faster)

### Calculate Quality Metrics

Compare interpolated video against ground truth:
```bash
python -m src.cli metrics interpolated.mp4 ground_truth.mp4
```

Output includes PSNR, SSIM, and VMAF scores with quality ratings.

### Benchmark Performance

Test processing speed at different resolutions:
```bash
python -m src.cli benchmark input.mp4
```

Specify resolutions:
```bash
python -m src.cli benchmark input.mp4 -r 720p -r 1080p -r 4k
```

### Create Test Data

Downsample high-FPS video to create synthetic test input:
```bash
python -m src.cli downsample 60fps.mp4 30fps.mp4 --skip 2
```

## Workflow Example

Complete workflow for quality evaluation:
```bash
python -m src.cli downsample gameplay_60fps.mp4 data/input/gameplay_30fps.mp4 --skip 2

python -m src.cli interpolate data/input/gameplay_30fps.mp4 data/output/gameplay_interp.mp4 --multi 2

python -m src.cli metrics data/output/gameplay_interp.mp4 gameplay_60fps.mp4
```

## Configuration

Edit `configs/default.yaml` to change default settings:
```yaml
model:
  version: "4.25"

interpolation:
  default_multi: 2
  scale: 1.0

output:
  codec: "libx264"
  crf: 18
```

## Logging

Logs are written to `logs/rife_YYYY-MM-DD.log`. Enable verbose output:
```bash
python -m src.cli --verbose interpolate input.mp4 output.mp4
```
