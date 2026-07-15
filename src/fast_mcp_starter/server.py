from __future__ import annotations

from typing import Literal

from mcp.server.fastmcp import FastMCP
from science_demo.science_tools import generate_random_points, plot_sine_wave

Transport = Literal["stdio", "streamable-http", "http"]


def create_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    json_response: bool = False,
    stateless_http: bool = True,
) -> FastMCP:
    mcp = FastMCP(
        "FastMCP Tool Server Starter",
        instructions=(
            "Expose package functions as MCP tools. Each tool receives an output_dir "
            "argument and returns structured artifact status."
        ),
        host=host,
        port=port,
        json_response=json_response,
        stateless_http=stateless_http,
    )

    mcp.tool()(generate_random_points)
    mcp.tool()(plot_sine_wave)
    return mcp


def run_server(
    *,
    transport: Transport = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
    json_response: bool = False,
) -> None:
    resolved_transport = "streamable-http" if transport == "http" else transport
    mcp = create_server(host=host, port=port, json_response=json_response)
    mcp.run(transport=resolved_transport)
