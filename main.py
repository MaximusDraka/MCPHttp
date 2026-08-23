from mcp.server.fastmcp import FastMCP
import os

PORT = os.environ.get("PORT", 10000)
API_KEY = os.environ.get("API_KEY", "default-key-change-me")

# Create an MCP server
mcp = FastMCP("web-search", host="0.0.0.0", port=PORT)

# Middleware to check API key
@mcp.server.middleware("before_request")
def check_api_key(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith(f"Bearer {API_KEY}"):
        raise ValueError("Invalid or missing API key")



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