"""Frame Interpolation Pipeline using RIFE"""
import argparse, os, sys, subprocess
import cv2

def get_video_info(path):
    cap = cv2.VideoCapture(path)
    info = {"width": int(cap.get(3)), "height": int(cap.get(4)), 
            "fps": cap.get(5), "frames": int(cap.get(7))}
    cap.release()
    return info

def interpolate(input_path, output_path, multi=2):
    info = get_video_info(input_path)
    print(f"Input: {info['width']}x{info['height']} @ {info['fps']:.1f} FPS → {info['fps']*multi:.1f} FPS")
    cmd = [sys.executable, "Practical-RIFE/inference_video.py", 
           f"--multi={multi}", f"--video={input_path}", f"--output={output_path}"]
    subprocess.run(cmd, check=True)
    print(f"✓ Output: {output_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True)
    p.add_argument("--output", "-o", required=True)
    p.add_argument("--multi", "-m", type=int, default=2, choices=[2,4,8])
    args = p.parse_args()
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    interpolate(args.input, args.output, args.multi)
