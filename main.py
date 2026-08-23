import asyncio
import os
from mcp.server.fastmcp import FastMCP
import uvicorn

PORT = int(os.environ.get("PORT", 8000))

# Create MCP server
mcp = FastMCP(name="web-search", stateless_http=True)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Get the FastAPI app from MCP
app = mcp.app


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        reload=False
    )