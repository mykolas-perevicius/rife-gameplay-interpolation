# Experimental Methodology

## 1. Research Design

This study employs a quantitative experimental design comparing AI-interpolated frames against ground-truth high-framerate recordings.

## 2. Dataset Collection

### 2.1 Recording Setup

**Hardware Configuration:**
- GPU: NVIDIA RTX 3090 (24GB VRAM)
- CPU: AMD Ryzen 9 5900X
- RAM: 64GB DDR4-3600
- Storage: NVMe SSD (sustained 3GB/s write)

**Recording Software:**
- NVIDIA ShadowPlay (hardware encoding)
- OBS Studio (software backup)

**Recording Parameters:**
- Resolution: 1920x1080 (native)
- Frame Rate: 60 FPS (ground truth)
- Bitrate: 50 Mbps CBR
- Codec: H.264 (NVENC)
- Audio: Disabled (reduces variables)

### 2.2 Game Selection

| Game | Genre | Motion Characteristics |
|------|-------|----------------------|
| Escape from Tarkov | Tactical FPS | Fast ADS, recoil, particle effects |
| ARC Raiders | Co-op Shooter | Large environments, explosions, AI movement |

### 2.3 Clip Selection Criteria

Each game contributes 5 clips of 60 seconds each, capturing:

1. **Low Motion**: Menu navigation, inventory management
2. **Medium Motion**: Walking, looting, ambient gameplay
3. **High Motion**: Combat, sprinting, vehicle movement
4. **Particle Heavy**: Explosions, smoke grenades, weather effects
5. **Camera Shake**: Recoil, damage feedback, environmental effects

## 3. Data Preparation

### 3.1 Ground Truth Extraction
```
60 FPS Recording (Native)
         │
         ▼
    Frame 0, 1, 2, 3, 4, 5, 6, 7, ...
```

### 3.2 Synthetic Input Generation

Extract every other frame to simulate 30 FPS capture:
```
60 FPS Recording
         │
    Extract even frames
         │
         ▼
30 FPS Synthetic (Frame 0, 2, 4, 6, ...)
```

### 3.3 Interpolation Target

Use RIFE to reconstruct odd frames:
```
30 FPS Input
         │
    RIFE Interpolation (2x)
         │
         ▼
60 FPS Interpolated (Frame 0, 1*, 2, 3*, 4, ...)
                          (* = AI generated)
```

## 4. Evaluation Protocol

### 4.1 Quantitative Metrics

For each interpolated video:

1. **PSNR**: Frame-by-frame comparison, report mean and std
2. **SSIM**: Structural similarity, report mean and std
3. **VMAF**: Perceptual quality, report mean and std

### 4.2 Temporal Analysis

Track metrics over time to identify:
- Scene change artifacts
- Motion-correlated quality drops
- Particle effect handling

### 4.3 Artifact Annotation

Manual review of 1000 frames per game:

| Artifact Type | Definition | Severity (1-3) |
|---------------|------------|----------------|
| Ghosting | Semi-transparent duplicates | Motion trails |
| Tearing | Discontinuous edges | Broken geometry |
| Blur | Loss of sharpness | Smeared details |
| Hallucination | Incorrect synthesis | Wrong content |

## 5. Performance Benchmarking

### 5.1 Inference Speed

Measure processing FPS at multiple resolutions:
- 1280x720 (720p)
- 1920x1080 (1080p)
- 2560x1440 (1440p)

### 5.2 Memory Usage

Monitor VRAM consumption during inference.

### 5.3 Real-time Viability

Calculate real-time ratio:
```
Real-time Ratio = Inference FPS / Video FPS
```

Ratio ≥ 1.0 indicates real-time capability.

## 6. Statistical Analysis

### 6.1 Descriptive Statistics

Report mean, median, standard deviation, and IQR for all metrics.

### 6.2 Correlation Analysis

Examine relationships between:
- Motion magnitude and quality metrics
- Particle density and artifact frequency
- Resolution and processing speed

## 7. Limitations

1. **Synthetic Degradation**: Extracting frames differs from native low-FPS capture
2. **Compression Artifacts**: Encoding may mask interpolation errors
3. **Game Selection**: Results may not generalize to all genres
4. **Subjective Assessment**: No human evaluation study conducted
