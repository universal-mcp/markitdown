
from universal_mcp.servers.server import SingleMCPServer

from universal_mcp_markitdown.app import MarkitdownApp

app_instance = MarkitdownApp()

mcp = SingleMCPServer(
    app_instance=app_instance,
    host="0.0.0.0"
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")


