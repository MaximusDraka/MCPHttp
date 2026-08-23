from mcp.server.fastmcp import FastMCP
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

PORT = os.environ.get("PORT", 10000)
API_KEY = os.environ.get("API_KEY", "default-key-change-me")

# Create an MCP server
mcp = FastMCP("web-search", host="0.0.0.0", port=PORT)

# Custom middleware for API key validation
class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow MCP protocol endpoints without auth check first
        if request.url.path == "/sse" or request.url.path == "/messages":
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith(f"Bearer {API_KEY}"):
                return JSONResponse(
                    {"error": "Invalid or missing API key"},
                    status_code=401
                )
        response = await call_next(request)
        return response

# Add middleware to the app
mcp.app.add_middleware(APIKeyMiddleware)



@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."




if __name__ == "__main__":
     mcp.run(transport="streamable-http")