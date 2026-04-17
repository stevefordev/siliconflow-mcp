from mcp.server.fastmcp import FastMCP
from . import images, videos, user, audio

# Initialize FastMCP server
mcp = FastMCP("siliconflow-mcp")

# Register Image Tools
mcp.tool()(images.generate_image)
mcp.tool()(images.edit_image)

# Register Video Tools
mcp.tool()(videos.submit_video_generation)
mcp.tool()(videos.get_video_status)
mcp.tool()(videos.generate_video)

# Register Audio Tools
mcp.tool()(audio.generate_speech)

# Register User & Model Tools
mcp.tool()(user.get_user_info)
mcp.tool()(user.list_models)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
