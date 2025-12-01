# API Reference

## Core Modules

### RIFEInterpolator

Main class for video frame interpolation.
```python
from src.core.interpolator import RIFEInterpolator

interpolator = RIFEInterpolator(model_version="4.25")

stats = interpolator.process(
    input_path="input.mp4",
    output_path="output.mp4",
    multi=2,
    scale=1.0,
    progress_callback=lambda pct: print(f"{pct}%")
)
```

**Parameters:**
- `model_version`: RIFE model version string

**Methods:**

`process(input_path, output_path, multi=2, scale=1.0, progress_callback=None)`
- `input_path`: Source video path
- `output_path`: Destination video path
- `multi`: Frame multiplication factor
- `scale`: Input resolution scale
- `progress_callback`: Optional function receiving progress percentage

**Returns:** Dictionary with processing statistics

### MetricsCalculator

Calculate video quality metrics.
```python
from src.core.metrics import MetricsCalculator

calc = MetricsCalculator(output_dir="results/metrics")

results = calc.calculate(
    interpolated="output.mp4",
    reference="ground_truth.mp4",
    metrics=["psnr", "ssim", "vmaf"]
)
```

**Methods:**

`calculate(interpolated, reference, metrics=None, output_path=None)`
- `interpolated`: Path to interpolated video
- `reference`: Path to ground truth video
- `metrics`: List of metrics to compute
- `output_path`: Optional JSON output path

**Returns:** Dictionary with metric scores

### Benchmarker

Performance benchmarking across resolutions.
```python
from src.core.benchmark import Benchmarker

bench = Benchmarker(output_dir="results/benchmarks")

results = bench.run(
    input_path="sample.mp4",
    resolutions=["720p", "1080p", "1440p"]
)

bench.save_results(results, "benchmark.json")
```

### FrameExtractor

Video frame manipulation utilities.
```python
from src.core.extractor import FrameExtractor

extractor = FrameExtractor()

stats = extractor.downsample(
    input_path="60fps.mp4",
    output_path="30fps.mp4",
    skip=2
)
```

## Utility Modules

### Logger

Configured logging with Loguru.
```python
from src.utils.logger import log, setup_logger

setup_logger(verbose=True)

log.info("Processing started")
log.success("Complete!")
log.error("Something failed")
```

### Config

Pydantic configuration management.
```python
from src.utils.config import Config

config = Config("configs/default.yaml")
print(config.model.version)
print(config.interpolation.default_multi)
```
