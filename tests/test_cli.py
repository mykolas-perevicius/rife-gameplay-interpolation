"""Basic CLI tests."""

import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    """Test CLI shows help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "RIFE" in result.output


def test_cli_info(runner):
    """Test info command."""
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "Python" in result.output
