# Science Demo

Demo science package imported by the MCP starter.

Requires Python 3.12+.

Public API:

```python
generate_random_points(output_dir: str, count: int = 30, seed: int = 42) -> ArtifactResult
plot_sine_wave(output_dir: str, num_points: int = 200) -> ArtifactResult
```

Both functions create files in `output_dir` and return typed structured content:

```json
{"status": "success", "files": ["..."], "message": "...", "metadata": {}}
```

`ArtifactResult` is a Pydantic model. FastMCP uses it to publish a concrete MCP
`outputSchema`, while LangGraph/LangChain MCP clients receive the same data as
structured tool content.
