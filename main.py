import os
from fastmcp import FastMCP

PORT = int(os.environ.get("PORT", 8000))

# Create MCP server
mcp = FastMCP(name="web-search")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@mcp.prompt
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=PORT)
