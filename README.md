# Science MCP Server Starter

Minimal starter code for wrapping science functions as MCP tools.

The science code stays normal Python. The MCP wrapper only imports the public
tool functions listed in `pyproject.toml` and exposes them through FastMCP.

This repo only defines the MCP server. Agent code lives in the client repo that
connects to it.

## Connect Science Code

1. Copy the MCP wrapper into the science repo root.

```text
mcp_server/
```

This repo uses `science_demo/` as the example science package.

2. Create normal Python functions in the science package.

```python
def plot_sine_wave(output_dir: str, num_points: int = 200):
    """Plot a sine wave and save it in output_dir."""
    ...
```

3. Export only the MCP tools from the science package `__init__.py`.

```python
from .science_tools import plot_sine_wave

__all__ = ["plot_sine_wave"]
```

Only names in `__all__` become MCP tools. Helper functions stay private. This
starter does not scan a repo for functions.

4. Add the MCP dependency and tool module config in `pyproject.toml`.

```toml
dependencies = [
    "mcp[cli]>=1.27,<2",
]

[tool.mcp-server]
tool_modules = ["your_science_package"]
```

5. Install the science repo.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

6. Connect an agent with one transport.

Use `stdio` for a local MCP server that the agent's MCP client starts for you.
Do not start the stdio server in a separate terminal. Configure the client with
the command and arguments to launch:

```json
{
  "science": {
    "transport": "stdio",
    "command": "python",
    "args": ["-m", "mcp_server", "--transport", "stdio"]
  }
}
```

Use `streamable-http` when the agent connects to an already running server.
Start the server in a terminal:

```bash
python -m mcp_server --transport streamable-http --host 127.0.0.1 --port 8000
```

Then point the agent at:

```text
http://127.0.0.1:8000/mcp
```

## Demo Tools

The demo science package exposes:

```python
generate_random_points(output_dir: str, count: int = 30, seed: int = 42) -> ArtifactResult
plot_sine_wave(output_dir: str, num_points: int = 200) -> ArtifactResult
```

The type hints, docstrings, and Pydantic constraints become the MCP tool schema
that external agents see.

Successful artifact tools return:

```json
{"status": "success", "files": ["..."], "message": "...", "metadata": {}}
```
