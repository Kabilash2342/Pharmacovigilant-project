import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Connect to MCP server
            await session.initialize()

            print("\nConnected to MCP server!")

            # Get available tools
            tools = await session.list_tools()

            print("\nAvailable MCP Tools:\n")

            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f"  {tool.description}")
                print()

            # Call an MCP tool
            print("Calling search_adverse_events_tool...\n")

            result = await session.call_tool(
                "search_adverse_events_tool",
                {
                    "drug_name": "Drug X",
                    "adverse_event": "Liver Injury"
                }
            )

            print("\nTool Result:\n")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())