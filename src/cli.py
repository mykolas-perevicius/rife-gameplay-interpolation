"""
RIFE Gameplay Interpolation CLI

A beautiful command-line interface for AI-powered frame interpolation.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich import box

from src.core.interpolator import RIFEInterpolator
from src.core.metrics import MetricsCalculator
from src.core.benchmark import Benchmarker
from src.utils.logger import setup_logger, log
from src.utils.config import Config

console = Console()

BANNER = """
[bold cyan]╦═╗╦╔═╗╔═╗[/]  [bold white]Gameplay Interpolation[/]
[bold cyan]╠╦╝║╠╣ ║╣ [/]  [dim]AI-Powered Frame Enhancement[/]
[bold cyan]╩╚═╩╚  ╚═╝[/]  [dim]v0.1.0 • CS 474 Project[/]
"""

def print_banner():
    console.print(Panel(BANNER, border_style="cyan", box=box.DOUBLE))

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--config", "-c", type=click.Path(), help="Config file path")
@click.pass_context
def cli(ctx, verbose, config):
    """🎮 RIFE Gameplay Interpolation - AI-powered frame enhancement for gaming videos."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = Config(config) if config else Config()
    setup_logger(verbose)
    print_banner()

@cli.command()
@click.argument("input_video", type=click.Path(exists=True))
@click.argument("output_video", type=click.Path())
@click.option("--multi", "-m", default=2, type=click.Choice(["2", "4", "8"]), help="Frame multiplier")
@click.option("--model", default="4.25", help="RIFE model version")
@click.option("--scale", "-s", default=1.0, type=float, help="Input scale factor (0.5 for half res)")
@click.pass_context
def interpolate(ctx, input_video, output_video, multi, model, scale):
    """🚀 Interpolate video frames using RIFE.
    
    Examples:
        rife interpolate gameplay.mp4 gameplay_60fps.mp4
        rife interpolate input.mp4 output.mp4 --multi 4
    """
    multi = int(multi)
    
    console.print(f"\n[bold green]►[/] Starting interpolation...\n")
    
    # Display settings
    table = Table(title="Settings", box=box.ROUNDED, border_style="blue")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Input", str(input_video))
    table.add_row("Output", str(output_video))
    table.add_row("Multiplier", f"{multi}x")
    table.add_row("Model", f"RIFE v{model}")
    table.add_row("Scale", f"{scale}")
    console.print(table)
    console.print()
    
    try:
        interpolator = RIFEInterpolator(model_version=model)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Processing frames...", total=100)
            
            def update_progress(pct):
                progress.update(task, completed=pct)
            
            stats = interpolator.process(
                input_video, 
                output_video, 
                multi=multi,
                scale=scale,
                progress_callback=update_progress
            )
        
        # Results
        console.print(f"\n[bold green]✓[/] Interpolation complete!\n")
        
        results = Table(title="Results", box=box.ROUNDED, border_style="green")
        results.add_column("Metric", style="cyan")
        results.add_column("Value", style="white")
        results.add_row("Input FPS", f"{stats['input_fps']:.2f}")
        results.add_row("Output FPS", f"{stats['output_fps']:.2f}")
        results.add_row("Frames", f"{stats['input_frames']} → {stats['output_frames']}")
        results.add_row("Processing Time", f"{stats['elapsed']:.1f}s")
        results.add_row("Speed", f"{stats['processing_fps']:.1f} fps")
        console.print(results)
        
        log.success(f"Output saved to: {output_video}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/] {e}")
        log.error(f"Interpolation failed: {e}")
        sys.exit(1)

@cli.command()
@click.argument("interpolated", type=click.Path(exists=True))
@click.argument("reference", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output JSON path")
@click.option("--metrics", "-m", multiple=True, default=["psnr", "ssim", "vmaf"], 
              help="Metrics to calculate")
@click.pass_context
def metrics(ctx, interpolated, reference, output, metrics):
    """📊 Calculate quality metrics (PSNR, SSIM, VMAF).
    
    Examples:
        rife metrics output.mp4 ground_truth.mp4
        rife metrics output.mp4 reference.mp4 -m psnr -m ssim
    """
    console.print(f"\n[bold green]►[/] Calculating quality metrics...\n")
    
    calc = MetricsCalculator()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Analyzing frames...", total=None)
        results = calc.calculate(interpolated, reference, list(metrics), output)
    
    console.print(f"\n[bold green]✓[/] Analysis complete!\n")
    
    # Results table
    table = Table(title="Quality Metrics", box=box.ROUNDED, border_style="green")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", style="white")
    table.add_column("Rating", style="yellow")
    
    if "psnr" in results:
        rating = "Excellent" if results["psnr"] > 35 else "Good" if results["psnr"] > 30 else "Fair"
        table.add_row("PSNR", f"{results['psnr']:.2f} dB", rating)
    if "ssim" in results:
        rating = "Excellent" if results["ssim"] > 0.97 else "Good" if results["ssim"] > 0.95 else "Fair"
        table.add_row("SSIM", f"{results['ssim']:.4f}", rating)
    if "vmaf" in results:
        rating = "Excellent" if results["vmaf"] > 90 else "Good" if results["vmaf"] > 80 else "Fair"
        table.add_row("VMAF", f"{results['vmaf']:.2f}", rating)
    
    console.print(table)
    
    if output:
        log.info(f"Results saved to: {output}")

@cli.command()
@click.argument("input_video", type=click.Path(exists=True))
@click.option("--resolutions", "-r", multiple=True, default=["720p", "1080p", "1440p"])
@click.option("--output", "-o", type=click.Path(), help="Output JSON path")
@click.pass_context
def benchmark(ctx, input_video, resolutions, output):
    """⚡ Benchmark interpolation performance.
    
    Examples:
        rife benchmark gameplay.mp4
        rife benchmark input.mp4 -r 720p -r 1080p -r 4k
    """
    console.print(f"\n[bold green]►[/] Running performance benchmark...\n")
    
    benchmarker = Benchmarker()
    results = benchmarker.run(input_video, list(resolutions))
    
    console.print(f"\n[bold green]✓[/] Benchmark complete!\n")
    
    # GPU info
    console.print(f"[bold]GPU:[/] {results['gpu']}")
    console.print(f"[bold]VRAM:[/] {results['vram']}\n")
    
    # Results table
    table = Table(title="Performance Results", box=box.ROUNDED, border_style="green")
    table.add_column("Resolution", style="cyan")
    table.add_column("Inference FPS", style="white")
    table.add_column("Real-time", style="yellow")
    table.add_column("Status", style="white")
    
    for r in results["benchmarks"]:
        status = "[green]✓[/]" if r["realtime"] else "[red]✗[/]"
        table.add_row(
            r["resolution"],
            f"{r['fps']:.1f}",
            f"{r['realtime_ratio']:.2f}x",
            status
        )
    
    console.print(table)
    
    if output:
        benchmarker.save_results(results, output)
        log.info(f"Results saved to: {output}")

@cli.command()
@click.argument("input_video", type=click.Path(exists=True))
@click.argument("output_video", type=click.Path())
@click.option("--skip", "-s", default=2, type=int, help="Keep every Nth frame")
@click.pass_context  
def downsample(ctx, input_video, output_video, skip):
    """📉 Create synthetic low-FPS test data.
    
    Extracts every Nth frame to simulate lower framerates.
    
    Examples:
        rife downsample 60fps.mp4 30fps.mp4 --skip 2
    """
    from src.core.extractor import FrameExtractor
    
    console.print(f"\n[bold green]►[/] Downsampling video (every {skip} frames)...\n")
    
    extractor = FrameExtractor()
    stats = extractor.downsample(input_video, output_video, skip)
    
    console.print(f"[bold green]✓[/] Done!")
    console.print(f"    {stats['input_fps']:.1f} FPS → {stats['output_fps']:.1f} FPS")
    console.print(f"    {stats['input_frames']} → {stats['output_frames']} frames")

@cli.command()
@click.option("--model", "-m", default="4.25", help="Model version to download")
@click.pass_context
def setup(ctx, model):
    """🔧 Download models and setup environment.
    
    Examples:
        rife setup
        rife setup --model 4.25.lite
    """
    from src.utils.setup import setup_environment
    
    console.print(f"\n[bold green]►[/] Setting up RIFE environment...\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Downloading components...", total=None)
        setup_environment(model, progress_callback=lambda msg: progress.update(task, description=msg))
    
    console.print(f"\n[bold green]✓[/] Setup complete! Run [cyan]rife interpolate --help[/] to get started.")

@cli.command()
@click.pass_context
def info(ctx):
    """ℹ️  Show system information and GPU status."""
    import torch
    import platform
    
    console.print(f"\n[bold cyan]System Information[/]\n")
    
    table = Table(box=box.ROUNDED, border_style="blue")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Python", platform.python_version())
    table.add_row("PyTorch", torch.__version__)
    table.add_row("CUDA Available", str(torch.cuda.is_available()))
    
    if torch.cuda.is_available():
        table.add_row("GPU", torch.cuda.get_device_name(0))
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        table.add_row("VRAM", f"{vram:.1f} GB")
        table.add_row("CUDA Version", torch.version.cuda or "N/A")
    
    table.add_row("Platform", platform.platform())
    
    console.print(table)

# Entry point
app = cli

if __name__ == "__main__":
    cli()
