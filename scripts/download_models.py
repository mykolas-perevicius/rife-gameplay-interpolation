"""Download RIFE Model Weights"""
import subprocess, urllib.request, sys
from pathlib import Path

def download():
    Path("train_log").mkdir(exist_ok=True)
    url = "https://github.com/hzwer/Practical-RIFE/releases/download/v4.25/flownet.pkl"
    out = Path("train_log/flownet.pkl")
    if out.exists():
        print("✓ Model exists"); return
    print("Downloading RIFE v4.25...")
    urllib.request.urlretrieve(url, out)
    print(f"✓ Saved to {out}")

def clone_rife():
    if Path("Practical-RIFE").exists():
        print("✓ Practical-RIFE exists"); return
    subprocess.run(["git", "clone", "https://github.com/hzwer/Practical-RIFE.git"])

if __name__ == "__main__":
    clone_rife()
    download()
