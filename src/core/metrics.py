"""Quality Metrics Calculator"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.utils.logger import log


class MetricsCalculator:
    """Calculate video quality metrics using ffmpeg-quality-metrics."""
    
    def __init__(self, output_dir: str = "results/metrics"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate(
        self,
        interpolated: str,
        reference: str,
        metrics: List[str] = None,
        output_path: Optional[str] = None
    ) -> dict:
        """
        Calculate quality metrics between two videos.
        
        Args:
            interpolated: Path to interpolated video
            reference: Path to ground-truth reference
            metrics: List of metrics (psnr, ssim, vmaf)
            output_path: Optional output JSON path
        
        Returns:
            dict with metric scores
        """
        if metrics is None:
            metrics = ["psnr", "ssim", "vmaf"]
        
        # Generate output path
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"metrics_{timestamp}.json"
        
        # Build command
        cmd = [
            "ffmpeg-quality-metrics",
            interpolated,
            reference,
            "--metrics"
        ] + metrics + [
            "-o", str(output_path),
            "-of", "json"
        ]
        
        log.debug(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            log.error(f"Metrics calculation failed: {result.stderr}")
            raise RuntimeError(f"ffmpeg-quality-metrics failed: {result.stderr}")
        
        # Parse results
        with open(output_path) as f:
            data = json.load(f)
        
        # Extract summary
        summary = {}
        global_stats = data.get("global", {})
        
        if "psnr" in global_stats:
            summary["psnr"] = global_stats["psnr"].get("psnr_avg", {}).get("mean", 0)
        
        if "ssim" in global_stats:
            summary["ssim"] = global_stats["ssim"].get("ssim_avg", {}).get("mean", 0)
        
        if "vmaf" in global_stats:
            summary["vmaf"] = global_stats["vmaf"].get("vmaf", {}).get("mean", 0)
        
        summary["output_file"] = str(output_path)
        
        log.info(f"Metrics calculated: PSNR={summary.get('psnr', 'N/A'):.2f}, "
                 f"SSIM={summary.get('ssim', 'N/A'):.4f}, VMAF={summary.get('vmaf', 'N/A'):.2f}")
        
        return summary
