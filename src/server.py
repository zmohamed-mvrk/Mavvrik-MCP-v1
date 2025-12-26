import sys
import os
import logging
from dotenv import load_dotenv

# Force Python to see the project root
current_file_path = os.path.abspath(__file__)
src_directory = os.path.dirname(current_file_path)
project_root = os.path.dirname(src_directory)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure Logging to Stderr (Copilot reads stdout, so logs must go to stderr)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("mavvrik-mcp")

load_dotenv()

def main():
    try:
        from mcp.server.fastmcp import FastMCP
        from src.tools.finops import register_finops
        
        # Initialize Server
        logger.info("Initializing Mavvrik MCP Server (v1 Service Mode)...")
        mcp = FastMCP("Mavvrik Cost Intelligence")

        # Register ONLY FinOps tools (Auth tools are removed)
        register_finops(mcp)
        logger.info("FinOps tools registered. Ready for queries.")
        
        # Run in stdio mode (Required for VS Code Copilot)
        mcp.run(transport="stdio")
        
    except Exception as e:
        logger.critical(f"Server crashed: {e}")
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()