import csv
import math
import random
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, validate_call


class ArtifactResult(BaseModel):
    """Result returned by tools."""

    status: Literal["success"]
    files: list[str]
    message: str
    metadata: dict[str, Any]


@validate_call
def generate_random_points(
    output_dir: Annotated[str, Field(min_length=1)],
    count: Annotated[int, Field(ge=1, le=1000)] = 30,
    seed: Annotated[int, Field(ge=0, le=1_000_000)] = 42,
) -> ArtifactResult:
    """Generate random point data and save it as a CSV in output_dir.

    Use this tool when a workflow needs a small deterministic dataset for
    downstream analysis or visualization.

    Args:
        output_dir: Required directory where the CSV should be written.
        count: Number of point rows to generate, from 1 to 1000.
        seed: Seed for deterministic random data, from 0 to 1000000.
    """
    outdir = Path(output_dir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)

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

    return ArtifactResult(
        status="success",
        files=[str(csv_path)],
        message="Generated random point CSV.",
        metadata={"count": count, "seed": seed},
    )


@validate_call
def plot_sine_wave(
    output_dir: Annotated[str, Field(min_length=1)],
    num_points: Annotated[int, Field(ge=2, le=1000)] = 200,
) -> ArtifactResult:
    """Plot a sine wave and save it as a PNG in output_dir.

    Use this tool when a workflow needs a simple generated plot artifact for
    downstream inspection or reporting.

    Args:
        output_dir: Required directory where the PNG should be written.
        num_points: Number of samples to plot, from 2 to 1000.
    """
    outdir = Path(output_dir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    plot_path = outdir / "sine_wave.png"

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

    return ArtifactResult(
        status="success",
        files=[str(plot_path)],
        message="Generated sine wave plot.",
        metadata={"num_points": num_points},
    )
