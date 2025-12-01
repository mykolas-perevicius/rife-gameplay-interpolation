"""Environment setup utilities."""

import subprocess
import urllib.request
from pathlib import Path
from typing import Callable, Optional

from src.utils.logger import log


MODEL_URLS = {
    "4.25": "https://github.com/hzwer/Practical-RIFE/releases/download/v4.25/flownet.pkl",
    "4.25.lite": "https://github.com/hzwer/Practical-RIFE/releases/download/v4.25/flownet_lite.pkl",
}


def setup_environment(
    model_version: str = "4.25",
    progress_callback: Optional[Callable[[str], None]] = None
):
    """Setup RIFE environment."""
    
    def update(msg: str):
        if progress_callback:
            progress_callback(f"[cyan]{msg}")
        log.info(msg)
    
    # Clone Practical-RIFE
    rife_path = Path("Practical-RIFE")
    if not rife_path.exists():
        update("Cloning Practical-RIFE...")
        subprocess.run(
            ["git", "clone", "https://github.com/hzwer/Practical-RIFE.git"],
            capture_output=True,
            check=True
        )
        log.success("Cloned Practical-RIFE")
    else:
        update("Practical-RIFE already exists")
    
    # Download model
    train_log = Path("train_log")
    train_log.mkdir(exist_ok=True)
    
    model_path = train_log / "flownet.pkl"
    
    if not model_path.exists():
        if model_version not in MODEL_URLS:
            raise ValueError(f"Unknown model version: {model_version}")
        
        url = MODEL_URLS[model_version]
        update(f"Downloading RIFE v{model_version}...")
        
        urllib.request.urlretrieve(url, model_path)
        log.success(f"Downloaded model to {model_path}")
    else:
        update("Model weights already exist")
    
    # Copy to Practical-RIFE
    rife_train_log = rife_path / "train_log"
    rife_train_log.mkdir(exist_ok=True)
    
    import shutil
    if not (rife_train_log / "flownet.pkl").exists():
        shutil.copy(model_path, rife_train_log / "flownet.pkl")
    
    update("Setup complete!")
