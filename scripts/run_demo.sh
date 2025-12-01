#!/bin/bash
set -e

echo "========================================"
echo "  RIFE Gameplay Interpolation Demo"
echo "========================================"
echo ""

cd "$(dirname "$0")/.."

echo "[1/6] Generating test videos..."
python scripts/generate_test_video.py

echo ""
echo "[2/6] System information..."
python -m src.cli info

echo ""
echo "[3/6] Downsampling 60fps to 30fps..."
python -m src.cli downsample data/ground_truth/test_60fps.mp4 data/input/test_synthetic_30fps.mp4 --skip 2

echo ""
echo "[4/6] Running interpolation (this may take a moment)..."
if [ -d "Practical-RIFE" ] && [ -f "train_log/flownet.pkl" ]; then
    python -m src.cli interpolate data/input/test_30fps.mp4 data/output/test_interpolated_60fps.mp4 --multi 2
else
    echo "  [SKIP] RIFE not set up. Run: python -m src.cli setup"
    echo "  Creating placeholder output..."
    cp data/input/test_30fps.mp4 data/output/test_interpolated_60fps.mp4 2>/dev/null || true
fi

echo ""
echo "[5/6] Calculating quality metrics..."
if command -v ffmpeg-quality-metrics &> /dev/null; then
    python -m src.cli metrics data/output/test_interpolated_60fps.mp4 data/ground_truth/test_60fps.mp4 || echo "  Metrics calculation skipped (videos may differ in length)"
else
    echo "  [SKIP] ffmpeg-quality-metrics not installed"
fi

echo ""
echo "[6/6] Demo complete!"
echo ""
echo "Generated files:"
ls -lh data/ground_truth/*.mp4 2>/dev/null || true
ls -lh data/input/*.mp4 2>/dev/null || true
ls -lh data/output/*.mp4 2>/dev/null || true
echo ""
echo "========================================"
