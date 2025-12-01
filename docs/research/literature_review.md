# Literature Review: Video Frame Interpolation

## 1. Introduction

Video frame interpolation (VFI) synthesizes intermediate frames between existing frames to increase temporal resolution. This technique has applications in slow-motion generation, frame rate upconversion, and video compression artifact reduction.

## 2. Traditional Approaches

### 2.1 Optical Flow Methods

Early VFI methods relied on explicit optical flow estimation followed by frame warping. Horn-Schunck (1981) and Lucas-Kanade (1981) established foundational techniques for motion estimation. These methods compute dense correspondence between frames but struggle with occlusions and large displacements.

### 2.2 Kernel-Based Methods

Kernel-based approaches (Niklaus et al., 2017) estimate spatially-adaptive convolution kernels that simultaneously capture motion and perform interpolation. While effective, kernel size limits the maximum motion that can be handled.

## 3. Deep Learning Approaches

### 3.1 DAIN (Depth-Aware Video Frame Interpolation)

Bao et al. (2019) introduced depth information to guide interpolation, improving handling of occlusions. The model explicitly reasons about which objects are in front, enabling better synthesis of disoccluded regions.

### 3.2 RIFE (Real-Time Intermediate Flow Estimation)

Huang et al. (2022) proposed RIFE, which directly estimates intermediate flows without computing bi-directional optical flow. Key innovations:

- **IFNet Architecture**: Lightweight CNN that estimates intermediate flow in a single forward pass
- **Privileged Distillation**: Training scheme using teacher networks with access to ground truth flow
- **Real-time Performance**: 30+ FPS for 720p 2x interpolation on consumer GPUs

RIFE achieves state-of-the-art quality while being 10-100x faster than previous methods.

### 3.3 FILM (Frame Interpolation for Large Motion)

Reda et al. (2022) from Google Research addressed large motion interpolation. Key contributions:

- **Scale-agnostic Feature Pyramid**: Shared weights across pyramid levels
- **Gram Matrix Loss**: Preserves texture during synthesis
- **Single Unified Network**: No dependency on external flow or depth networks

FILM excels at interpolating between near-duplicate photos with large temporal gaps.

## 4. Quality Metrics

### 4.1 PSNR (Peak Signal-to-Noise Ratio)

Measures pixel-level reconstruction accuracy. Computed as:
```
PSNR = 10 * log10(MAX² / MSE)
```

Typical ranges: 25-35 dB (higher is better). Limited correlation with perceptual quality.

### 4.2 SSIM (Structural Similarity Index)

Wang et al. (2004) proposed SSIM to capture perceptual similarity through luminance, contrast, and structure comparisons. Range: 0-1 (higher is better).

### 4.3 VMAF (Video Multimethod Assessment Fusion)

Netflix's machine learning-based metric trained on human quality judgments. Combines multiple elementary metrics using SVM regression. Range: 0-100 (higher is better). Best correlation with human perception for video streaming.

## 5. Gaming-Specific Challenges

Video game footage presents unique challenges for frame interpolation:

1. **Particle Effects**: Explosions, smoke, and muzzle flashes have stochastic motion patterns
2. **HUD Elements**: Static overlays should not be interpolated
3. **Camera Shake**: Rapid view changes during action sequences
4. **Scene Cuts**: Abrupt transitions between gameplay states
5. **High Contrast**: HDR-like rendering with bright highlights

## 6. Practical-RIFE Versions

The Practical-RIFE repository maintains production-optimized models:

| Version | Date | Notes |
|---------|------|-------|
| v4.25 | Sep 2024 | Additional flow blocks, improved anime handling |
| v4.22 | Aug 2024 | Suitable for diffusion model post-processing |
| v4.17 | May 2024 | Gram loss from FILM for texture preservation |
| v4.15 | Mar 2024 | Balanced quality/performance |

## 7. References

1. Bao, W., et al. "Depth-Aware Video Frame Interpolation." CVPR 2019.
2. Huang, Z., et al. "RIFE: Real-Time Intermediate Flow Estimation for Video Frame Interpolation." ECCV 2022.
3. Niklaus, S., et al. "Video Frame Interpolation via Adaptive Separable Convolution." ICCV 2017.
4. Reda, F., et al. "FILM: Frame Interpolation for Large Motion." ECCV 2022.
5. Wang, Z., et al. "Image Quality Assessment: From Error Visibility to Structural Similarity." IEEE TIP 2004.
