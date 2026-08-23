import os
from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

PORT = int(os.environ.get("PORT", 8000))
API_KEY = os.environ.get("API_KEY", "change-me")

# Create MCP server
mcp = FastMCP(name="web-search")


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {API_KEY}":
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)


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
    import uvicorn
    from starlette.applications import Starlette

    # Get the underlying Starlette app from FastMCP and add middleware
    app = mcp.http_app()
    app.add_middleware(APIKeyMiddleware)

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
