# Artifact Taxonomy for Frame Interpolation

## Overview

This document defines the classification system used for annotating interpolation artifacts in gameplay footage.

## Artifact Categories

### 1. Ghosting

**Definition**: Semi-transparent copies of objects appearing along their motion trajectory.

**Causes**:
- Incorrect flow estimation for fast-moving objects
- Blending of warped frames without proper occlusion handling

**Severity Levels**:
- Level 1: Faint trails, only visible on close inspection
- Level 2: Noticeable trails that don't obscure content
- Level 3: Prominent trails affecting visual clarity

**Common Triggers**:
- Fast-moving projectiles
- Quick weapon swaps
- Rapid character movement

### 2. Tearing

**Definition**: Discontinuities in object boundaries where edges don't align.

**Causes**:
- Flow estimation failures at object boundaries
- Occlusion/disocclusion mishandling

**Severity Levels**:
- Level 1: Minor edge misalignment
- Level 2: Visible breaks in continuous lines
- Level 3: Severe geometric distortion

**Common Triggers**:
- HUD elements during camera motion
- Weapon models during ADS
- Character limbs during animation

### 3. Motion Blur (Excessive)

**Definition**: Unnatural smearing of details beyond intended motion blur.

**Causes**:
- Flow averaging in high-motion regions
- Interpolation between significantly different frames

**Severity Levels**:
- Level 1: Slight softening of moving edges
- Level 2: Noticeable blur affecting readability
- Level 3: Severe blur obscuring important details

**Common Triggers**:
- Rapid camera rotation
- Vehicle movement
- Explosion shockwaves

### 4. Warping

**Definition**: Spatial distortion of objects or textures.

**Causes**:
- Non-rigid motion assumptions failing
- Flow field discontinuities

**Severity Levels**:
- Level 1: Subtle shape changes
- Level 2: Noticeable stretching/compression
- Level 3: Severe deformation breaking object identity

**Common Triggers**:
- Particle systems
- Cloth/hair physics
- Water/fluid effects

### 5. Hallucination

**Definition**: Generation of content not present in source frames.

**Causes**:
- Disocclusion filling with incorrect content
- Pattern completion errors

**Severity Levels**:
- Level 1: Minor texture inconsistencies
- Level 2: Incorrect but plausible content
- Level 3: Clearly wrong or impossible content

**Common Triggers**:
- Objects entering/exiting frame
- Characters moving behind cover
- Large camera translations

### 6. Scene Change Artifacts

**Definition**: Blending of frames from different scenes.

**Causes**:
- Missing scene change detection
- Cut detection threshold too high

**Severity Levels**:
- Level 1: Brief flash
- Level 2: Visible frame blending
- Level 3: Extended incorrect interpolation

**Common Triggers**:
- Death/respawn transitions
- Loading screen boundaries
- Cutscene transitions

## Annotation Protocol

### Frame Selection

Sample frames at regular intervals:
- Every 100th frame for general survey
- Dense sampling (every frame) around detected issues

### Annotation Format
```json
{
  "frame_number": 1234,
  "timestamp": "00:00:41.400",
  "artifacts": [
    {
      "type": "ghosting",
      "severity": 2,
      "location": "center",
      "description": "Player weapon showing motion trail during sprint"
    }
  ]
}
```

### Quality Thresholds

| Rating | Artifacts per 1000 frames | Description |
|--------|--------------------------|-------------|
| Excellent | < 5 | Imperceptible in normal viewing |
| Good | 5-20 | Minor issues, acceptable quality |
| Fair | 20-50 | Noticeable but usable |
| Poor | > 50 | Significant quality degradation |
