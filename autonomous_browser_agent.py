
import asyncio

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv(override=True)


async def main():

    # =====================================
    # STEP 1: CREATE MCP CLIENT
    # =====================================

    print("\nConnecting to Playwright MCP...")

    client = MultiServerMCPClient({
        "playwright": {
            "command": "npx",
            "args": [
                "-y",
                "@playwright/mcp@latest",
                "--isolated"
            ],
            "transport": "stdio",
        }
    })

    # =====================================
    # STEP 2: OPEN PERSISTENT MCP SESSION
    # =====================================

    async with client.session("playwright") as session:

        print("MCP session established!")

        # Load tools from this session
        all_tools = await load_mcp_tools(session)

        print("\nAvailable MCP tools:", len(all_tools))

        # Select only two browser tools initially
        selected_names = [
            "browser_navigate",
            "browser_snapshot"
        ]

        tools = [
            tool for tool in all_tools
            if tool.name in selected_names
        ]

        print("\nTools provided to the agent:")

        for tool in tools:
            print("-", tool.name)

        # =================================
        # STEP 3: INITIALIZE GROQ MODEL
        # =================================

        model = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0
        )

        # =================================
        # STEP 4: CREATE AUTONOMOUS AGENT
        # =================================

        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt="""
            You are an autonomous web research assistant.

            You have access to browser navigation
            and webpage inspection tools.

            Your responsibilities:

            1. Understand the user's research request.
            2. Decide when to navigate to a website.
            3. Use browser_snapshot to inspect page content.
            4. Use the available tools when necessary.
            5. Summarize information actually retrieved.

            Rules:

            - Do not invent website content.
            - Do not claim that a website was visited
              unless the browser tool was called.
            - If a website cannot be accessed,
              clearly explain the limitation.
            - Do not perform purchases, submissions,
              or other external actions.
            """
        )

        # =================================
        # STEP 5: USER INPUT
        # =================================

        query = input("\nWhat should I research? ")

        # =================================
        # STEP 6: INVOKE AUTONOMOUS AGENT
        # =================================

        print("\nAgent is researching...\n")

        result = await agent.ainvoke({
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        })

        # =================================
        # STEP 7: DISPLAY RESULT
        # =================================

        print("\n========== RESEARCH REPORT ==========\n")

        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
