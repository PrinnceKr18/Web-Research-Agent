
import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq

load_dotenv(override=True)


def extract_text(result):
    """Extract text from MCP response content."""
    if result.isError:
        raise RuntimeError(f"MCP tool error: {result.content}")

    return "\n".join(
        item.text
        for item in result.content
        if hasattr(item, "text")
    )


async def main():

    # =====================================
    # STEP 1: CONNECT TO PLAYWRIGHT MCP
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
    # STEP 2: GET WEBSITE URL
    # =====================================

    url = input("\nEnter website URL: ").strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # =====================================
    # STEP 3: OPEN A PERSISTENT MCP SESSION
    # =====================================

    async with client.session("playwright") as session:

        print("\nMCP session established!")

        # =================================
        # STEP 4: NAVIGATE TO WEBSITE
        # =================================

        print("\nOpening website...")

        navigation_result = await session.call_tool(
            "browser_navigate",
            {"url": url}
        )

        navigation_text = extract_text(navigation_result)

        print("\nNavigation result:")
        print(navigation_text)

        # =================================
        # STEP 5: EXTRACT PAGE CONTENT
        # =================================

        print("\nExtracting webpage content...")

        extraction_result = await session.call_tool(
            "browser_evaluate",
            {
                "function": """() => {
                    return {
                        title: document.title,
                        url: window.location.href,
                        text: document.body
                            ? document.body.innerText
                            : ""
                    };
                }"""
            }
        )

        page_content = extract_text(extraction_result)

        print("\n========== EXTRACTED CONTENT ==========\n")
        print(page_content[:3000])

        if not page_content.strip():
            print("\nNo webpage content was extracted.")
            return

    # =====================================
    # STEP 6: INITIALIZE GROQ
    # =====================================

    print("\nGenerating research summary...")

    model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    # =====================================
    # STEP 7: PREPARE RESEARCH PROMPT
    # =====================================

    prompt = f"""
    You are an expert web research assistant.

    Analyze the following extracted webpage content.

    Website URL:
    {url}

    Navigation information:
    {navigation_text}

    Extracted webpage content:
    {page_content[:20000]}

    Provide the following:

    1. Main topic
    2. Detailed summary
    3. Important sections
    4. Key information
    5. Useful links, if available
    6. Important news or updates, if available

    Rules:
    - Use only the supplied webpage information.
    - Do not invent facts.
    - If the content is incomplete, mention it.
    """

    # =====================================
    # STEP 8: GENERATE SUMMARY
    # =====================================

    response = await model.ainvoke(prompt)

    # =====================================
    # STEP 9: DISPLAY REPORT
    # =====================================

    print("\n")
    print("=" * 55)
    print("              WEB RESEARCH REPORT")
    print("=" * 55)

    print("\nWebsite:", url)

    print("\nResearch Summary:\n")

    print(response.content)

    print("\n" + "=" * 55)
    print("              RESEARCH COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
