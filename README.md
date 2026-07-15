# FastMCP Tool Server Starter

Tiny FastMCP server that imports public functions from a science package and exposes them as MCP tools.

Requires Python 3.12+.

## Install

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./science-demo
pip install -e .
```

Or with `uv` that is faster and tidy than pip, but optional: 

```bash
uv sync
```

## Run

For agents that launch the server as a subprocess:

```bash
fast-mcp-starter --transport stdio
```

For agents that connect to a running MCP URL:

```bash
fast-mcp-starter --transport streamable-http --host 127.0.0.1 --port 8000
```

Endpoint:

```text
http://127.0.0.1:8000/mcp
```

## Test With A LangGraph Agent

See [notebooks/test_with_agent.ipynb](notebooks/test_with_agent.ipynb) for a
small external LangGraph agent that connects to this MCP server.

## Hook In Your Repo

Expose normal public Python functions in your external package, add that package as a dependency in [pyproject.toml](pyproject.toml#L11), then import and register those functions in [server.py](src/fast_mcp_starter/server.py#L6) and [server.py](src/fast_mcp_starter/server.py#L31-L32).

Keep `science-demo` as a working example while you add your own repo. Delete it later only if you do not want the demo tools.

This starter does that with:

```python
from science_demo.science_tools import generate_random_points, plot_sine_wave

mcp.tool()(generate_random_points)
mcp.tool()(plot_sine_wave)
```

## Demo Tools

The local `science-demo` package exposes:

```python
generate_random_points(output_dir: str, count: int = 30, seed: int = 42) -> ArtifactResult
plot_sine_wave(output_dir: str, num_points: int = 200) -> ArtifactResult
```

Both return typed structured content:

```json
{"status": "success", "files": ["..."], "message": "...", "metadata": {}}
```


## Test

```bash
python -m pytest
```
