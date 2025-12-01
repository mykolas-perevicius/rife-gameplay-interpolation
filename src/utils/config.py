"""Configuration management."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class ModelConfig(BaseModel):
    version: str = "4.25"
    weights_path: str = "train_log/flownet.pkl"


class InterpolationConfig(BaseModel):
    default_multi: int = 2
    scale: float = 1.0


class Config(BaseModel):
    """Application configuration."""
    
    model: ModelConfig = ModelConfig()
    interpolation: InterpolationConfig = InterpolationConfig()
    
    def __init__(self, config_path: Optional[str] = None, **kwargs):
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                data = yaml.safe_load(f)
            super().__init__(**data, **kwargs)
        else:
            super().__init__(**kwargs)
