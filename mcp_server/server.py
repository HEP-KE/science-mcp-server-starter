import importlib
from pathlib import Path
import tomllib
from typing import Literal

from mcp.server.fastmcp import FastMCP

Transport = Literal["stdio", "streamable-http"]


def pyproject_toml() -> Path:
    for directory in Path(__file__).resolve().parents:
        path = directory / "pyproject.toml"
        if path.exists():
            return path
    raise FileNotFoundError("Could not find pyproject.toml")


def configured_tool_module_names() -> list[str]:
    config = tomllib.loads(pyproject_toml().read_text(encoding="utf-8"))
    return list(config["tool"]["mcp-server"]["tool_modules"])


def load_tool_modules():
    return [
        importlib.import_module(module_name)
        for module_name in configured_tool_module_names()
    ]


def create_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> FastMCP:
    mcp = FastMCP(
        "Science MCP Server",
        instructions=(
            "Expose configured science functions as MCP tools. Tools that write files "
            "accept an output_dir argument and return structured artifact metadata."
        ),
        host=host,
        port=port,
    )

    for tool_module in load_tool_modules():
        for name in tool_module.__all__:
            mcp.tool()(getattr(tool_module, name))
    return mcp


def run_server(
    *,
    transport: Transport = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    mcp = create_server(host=host, port=port)
    mcp.run(transport=transport)
