from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from fast_mcp_starter.server import create_server


def test_create_server_registers_only_public_science_tools() -> None:
    mcp = create_server()

    tools = asyncio.run(mcp.list_tools())
    tool_names = {tool.name for tool in tools}

    assert tool_names == {"generate_random_points", "plot_sine_wave"}


def test_registered_tools_expose_docstrings_and_input_schemas() -> None:
    mcp = create_server()

    tools = asyncio.run(mcp.list_tools())
    by_name = {tool.name: tool for tool in tools}

    random_points = by_name["generate_random_points"]
    assert "Generate random point data" in random_points.description
    assert "count: Number of point rows" in random_points.description
    assert random_points.inputSchema["required"] == ["output_dir"]
    assert random_points.inputSchema["properties"]["output_dir"]["type"] == "string"
    assert random_points.inputSchema["properties"]["count"]["default"] == 30
    assert random_points.inputSchema["properties"]["seed"]["default"] == 42

    assert random_points.outputSchema["type"] == "object"
    assert random_points.outputSchema["required"] == [
        "status",
        "files",
        "message",
        "metadata",
    ]
    assert random_points.outputSchema["properties"]["status"]["const"] == "success"
    assert random_points.outputSchema["properties"]["files"]["type"] == "array"
    assert random_points.outputSchema["properties"]["message"]["type"] == "string"
    assert random_points.outputSchema["properties"]["metadata"]["type"] == "object"

    sine_plot = by_name["plot_sine_wave"]
    assert "Plot a sine wave" in sine_plot.description
    assert "num_points: Number of samples" in sine_plot.description
    assert sine_plot.inputSchema["required"] == ["output_dir"]
    assert sine_plot.inputSchema["properties"]["output_dir"]["type"] == "string"
    assert sine_plot.inputSchema["properties"]["num_points"]["default"] == 200
    assert sine_plot.outputSchema == random_points.outputSchema


def test_mcp_tool_call_returns_structured_result_and_writes_file(tmp_path: Path) -> None:
    async def call_tool() -> dict:
        mcp = create_server()
        _content, structured = await mcp.call_tool(
            "generate_random_points",
            {"output_dir": str(tmp_path), "count": 4, "seed": 123},
        )
        return structured

    result = asyncio.run(call_tool())

    assert result["status"] == "success"
    assert result["metadata"] == {"count": 4, "seed": 123}

    csv_path = Path(result["files"][0])
    assert csv_path.exists()
    assert csv_path.parent == tmp_path.resolve()


def test_mcp_tool_validation_failure_is_reported_as_tool_error(tmp_path: Path) -> None:
    async def call_tool() -> None:
        mcp = create_server()
        await mcp.call_tool(
            "generate_random_points",
            {"output_dir": str(tmp_path), "count": 0},
        )

    with pytest.raises(ToolError, match="count must be at least 1"):
        asyncio.run(call_tool())
