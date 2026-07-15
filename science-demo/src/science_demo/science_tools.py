from __future__ import annotations

import csv
import math
import os
import random
import tempfile
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel


class ArtifactResult(BaseModel):
    """Success result returned by artifact-producing MCP tools."""

    status: Literal["success"]
    files: list[str]
    message: str
    metadata: dict[str, Any]


def generate_random_points(
    output_dir: str,
    count: int = 30,
    seed: int = 42,
) -> ArtifactResult:
    """Generate random point data and save it as a CSV in output_dir.

    Use this tool when a workflow needs a small deterministic dataset for
    downstream analysis or visualization.

    Args:
        output_dir: Directory where the CSV should be written.
        count: Number of point rows to generate. Must be at least 1.
        seed: Seed for deterministic random data.
    """
    csv_path = _write_random_points_csv(
        output_dir=output_dir,
        count=count,
        seed=seed,
    )
    return ArtifactResult(
        status="success",
        files=[str(csv_path)],
        message="Generated random point CSV.",
        metadata={"count": count, "seed": seed},
    )


def plot_sine_wave(
    output_dir: str,
    num_points: int = 200,
) -> ArtifactResult:
    """Plot a sine wave and save it as a PNG in output_dir.

    Use this tool when a workflow needs a simple generated plot artifact for
    downstream inspection or reporting.

    Args:
        output_dir: Directory where the PNG should be written.
        num_points: Number of samples to plot. Must be at least 2.
    """
    plot_path = _write_sine_plot(output_dir=output_dir, num_points=num_points)
    return ArtifactResult(
        status="success",
        files=[str(plot_path)],
        message="Generated sine wave plot.",
        metadata={"num_points": num_points},
    )


def _write_random_points_csv(
    *,
    output_dir: str,
    count: int,
    seed: int,
) -> Path:
    if count < 1:
        raise ValueError("count must be at least 1")

    outdir = _ensure_output_dir(output_dir)
    csv_path = outdir / "random_points.csv"
    rng = random.Random(seed)

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=("index", "x", "y"))
        writer.writeheader()
        for index in range(count):
            writer.writerow(
                {
                    "index": index,
                    "x": f"{rng.random():.8f}",
                    "y": f"{rng.random():.8f}",
                }
            )

    return csv_path


def _write_sine_plot(*, output_dir: str, num_points: int) -> Path:
    if num_points < 2:
        raise ValueError("num_points must be at least 2")

    outdir = _ensure_output_dir(output_dir)
    plot_path = outdir / "sine_wave.png"

    _prepare_matplotlib_cache()
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    xs = [(2 * math.pi * index) / (num_points - 1) for index in range(num_points)]
    ys = [math.sin(x) for x in xs]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xs, ys, linewidth=2)
    ax.set_title("Sine wave")
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)

    return plot_path


def _ensure_output_dir(output_dir: str) -> Path:
    if not output_dir.strip():
        raise ValueError("output_dir must not be empty")

    outdir = Path(output_dir).expanduser().resolve()
    if outdir.exists() and not outdir.is_dir():
        raise NotADirectoryError(f"output_dir is not a directory: {outdir}")
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


def _prepare_matplotlib_cache() -> None:
    cache_dir = Path(tempfile.gettempdir()) / "science-demo-matplotlib"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
