import contextlib
from fastapi import FastAPI, Header
from mcp.server.fastmcp import FastMCP
import os

PORT = os.environ.get("PORT", 10000)
API_KEY = os.environ.get("API_KEY", "default-key-change-me")

# Create an MCP server with stateless HTTP
mcp = FastMCP(name="web-search", stateless_http=True)


# API Key validation decorator
def require_api_key(authorization: str = Header(None)):
    if not authorization or not authorization.startswith(f"Bearer {API_KEY}"):
        raise ValueError("Invalid or missing API key")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
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


# Create FastAPI app with proper lifespan
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/", mcp.streamable_http_app())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)