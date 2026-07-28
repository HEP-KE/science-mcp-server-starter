# MCP Server Wrapper

Copy this directory into the root of a science repo.

1. Export MCP tools from the science package `__init__.py`.

```python
from .science_tools import my_tool

__all__ = ["my_tool"]
```

2. Add the MCP dependency and tool module config in `pyproject.toml`.

```toml
dependencies = [
    "mcp[cli]>=1.27,<2",
]

[tool.mcp-server]
tool_modules = ["my_science_package"]
```

3. Install the science repo.

```bash
pip install -e .
```

4. Connect an agent with one transport.

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
