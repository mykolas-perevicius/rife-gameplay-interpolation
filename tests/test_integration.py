import pytest
import subprocess
import sys
from pathlib import Path


class TestCLI:
    def run_cli(self, *args):
        cmd = [sys.executable, "-m", "src.cli"] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    
    def test_help(self):
        result = self.run_cli("--help")
        assert result.returncode == 0
        assert "RIFE" in result.stdout
    
    def test_info(self):
        result = self.run_cli("info")
        assert result.returncode == 0
        assert "Python" in result.stdout
    
    def test_interpolate_help(self):
        result = self.run_cli("interpolate", "--help")
        assert result.returncode == 0
        assert "multi" in result.stdout
    
    def test_metrics_help(self):
        result = self.run_cli("metrics", "--help")
        assert result.returncode == 0
    
    def test_benchmark_help(self):
        result = self.run_cli("benchmark", "--help")
        assert result.returncode == 0
