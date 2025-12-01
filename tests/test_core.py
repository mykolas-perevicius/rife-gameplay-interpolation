import pytest
import os
import tempfile
from pathlib import Path


class TestInterpolator:
    def test_import(self):
        from src.core.interpolator import RIFEInterpolator
        assert RIFEInterpolator is not None
    
    def test_video_info(self):
        from src.core.interpolator import RIFEInterpolator
        
        test_video = Path("data/input/test_30fps.mp4")
        if not test_video.exists():
            pytest.skip("Test video not generated")
        
        interpolator = RIFEInterpolator.__new__(RIFEInterpolator)
        info = interpolator.get_video_info(str(test_video))
        
        assert "width" in info
        assert "height" in info
        assert "fps" in info
        assert "frames" in info
        assert info["fps"] > 0


class TestMetrics:
    def test_import(self):
        from src.core.metrics import MetricsCalculator
        assert MetricsCalculator is not None


class TestBenchmark:
    def test_import(self):
        from src.core.benchmark import Benchmarker
        assert Benchmarker is not None
    
    def test_gpu_info(self):
        from src.core.benchmark import Benchmarker
        
        bench = Benchmarker()
        info = bench.get_gpu_info()
        
        assert "gpu" in info
        assert "vram" in info


class TestExtractor:
    def test_import(self):
        from src.core.extractor import FrameExtractor
        assert FrameExtractor is not None


class TestConfig:
    def test_default_config(self):
        from src.utils.config import Config
        
        config = Config()
        assert config.model.version == "4.25"
        assert config.interpolation.default_multi == 2
    
    def test_load_yaml(self):
        from src.utils.config import Config
        
        config_path = Path("configs/default.yaml")
        if config_path.exists():
            config = Config(str(config_path))
            assert config.model.version is not None
