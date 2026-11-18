
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    client = MultiServerMCPClient({
        "playwright": {
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--isolated"],
            "transport": "stdio",
        }
    })

    tools = await client.get_tools()

    # Print all available MCP tools
    print("\n========== AVAILABLE MCP TOOLS ==========")

    for index, tool in enumerate(tools, start=1):
        print(f"\n{index}. Tool name: {tool.name}")
        print("Description:", tool.description[:500])
        print("Input schema:", tool.args_schema)

    print("\nTotal tools:", len(tools))


if __name__ == "__main__":
    asyncio.run(main())
