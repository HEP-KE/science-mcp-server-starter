from __future__ import annotations

import csv
from pathlib import Path

import pytest

from science_demo.science_tools import generate_random_points, plot_sine_wave


def _read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def test_generate_random_points_writes_deterministic_csv(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    first = generate_random_points(str(first_dir), count=3, seed=7)
    second = generate_random_points(str(second_dir), count=3, seed=7)

    assert first.status == "success"
    assert first.metadata == {"count": 3, "seed": 7}
    assert len(first.files) == 1

    first_csv = Path(first.files[0])
    second_csv = Path(second.files[0])
    assert first_csv.exists()
    assert second_csv.exists()
    assert first_csv.name == "random_points.csv"

    first_rows = _read_csv_rows(first_csv)
    second_rows = _read_csv_rows(second_csv)

    assert first_rows == second_rows
    assert [row["index"] for row in first_rows] == ["0", "1", "2"]
    assert set(first_rows[0]) == {"index", "x", "y"}
    for row in first_rows:
        assert 0 <= float(row["x"]) <= 1
        assert 0 <= float(row["y"]) <= 1


def test_generate_random_points_creates_nested_output_dir(tmp_path: Path) -> None:
    output_dir = tmp_path / "nested" / "agent-run-001"

    result = generate_random_points(str(output_dir), count=2, seed=11)

    assert result.status == "success"
    csv_path = Path(result.files[0])

    assert output_dir.is_dir()
    assert csv_path.parent == output_dir.resolve()
    assert len(_read_csv_rows(csv_path)) == 2


def test_generate_random_points_reports_validation_error(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="count must be at least 1"):
        generate_random_points(str(tmp_path), count=0)


def test_generate_random_points_reports_output_dir_error(tmp_path: Path) -> None:
    file_path = tmp_path / "not-a-directory"
    file_path.write_text("already a file", encoding="utf-8")

    with pytest.raises(NotADirectoryError, match="output_dir is not a directory"):
        generate_random_points(str(file_path), count=2)


def test_plot_sine_wave_writes_png_with_metadata(tmp_path: Path) -> None:
    output_dir = tmp_path / "plots"

    result = plot_sine_wave(str(output_dir), num_points=20)

    assert result.status == "success"
    assert result.metadata == {"num_points": 20}
    assert len(result.files) == 1

    plot_path = Path(result.files[0])
    assert plot_path.exists()
    assert plot_path.name == "sine_wave.png"
    assert plot_path.stat().st_size > 0
    assert plot_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_plot_sine_wave_reports_validation_error(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="num_points must be at least 2"):
        plot_sine_wave(str(tmp_path), num_points=1)
