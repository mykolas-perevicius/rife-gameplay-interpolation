"""Quality Metrics Calculator - PSNR, SSIM, VMAF"""
import argparse, subprocess, json, os
from datetime import datetime

def calculate_metrics(interp, ref, output_dir="results/metrics"):
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"{output_dir}/metrics_{ts}.json"
    cmd = ["ffmpeg-quality-metrics", interp, ref, "--metrics", "psnr", "ssim", "vmaf", "-o", out, "-of", "json"]
    subprocess.run(cmd, check=True)
    with open(out) as f: data = json.load(f)
    g = data.get("global", {})
    print(f"PSNR: {g.get('psnr',{}).get('psnr_avg',{}).get('mean',0):.2f} dB")
    print(f"SSIM: {g.get('ssim',{}).get('ssim_avg',{}).get('mean',0):.4f}")
    print(f"VMAF: {g.get('vmaf',{}).get('vmaf',{}).get('mean',0):.2f}")
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--interpolated", "-i", required=True)
    p.add_argument("--reference", "-r", required=True)
    args = p.parse_args()
    calculate_metrics(args.interpolated, args.reference)
