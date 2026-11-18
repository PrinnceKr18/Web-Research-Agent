
import asyncio
import json

from tavily import TavilyClient
from langchain_mcp_adapters.client import MultiServerMCPClient

from url_manager import process_search_results


# --------------------------------
# STEP 1: SEARCH THE WEB
# --------------------------------

def search_web(query):

    client = TavilyClient()

    response = client.search(
        query=query,
        max_results=5
    )

    return response["results"]


# --------------------------------
# STEP 2: EXTRACT MCP RESULT TEXT
# --------------------------------

def extract_text(result):

    if result.isError:
        raise RuntimeError(f"MCP error: {result.content}")

    return "\n".join(
        item.text
        for item in result.content
        if hasattr(item, "text")
    )


# --------------------------------
# STEP 3: VISIT MULTIPLE WEBSITES
# --------------------------------

async def research_websites(websites):

    collected_data = []

    client = MultiServerMCPClient({
        "playwright": {
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--isolated"],
            "transport": "stdio",
        }
    })

    # Keep one persistent browser session
    async with client.session("playwright") as session:

        for index, website in enumerate(websites, start=1):

            url = website["url"]

            print(f"\nVisiting website {index}: {url}")

            try:

                # Navigate to website
                navigation_result = await session.call_tool(
                    "browser_navigate",
                    {"url": url}
                )

                navigation_text = extract_text(navigation_result)

                print("Navigation completed.")

                # Extract webpage content
                snapshot_result = await session.call_tool(
                    "browser_snapshot",
                    {}
                )

                page_content = extract_text(snapshot_result)

                # Store extracted information
                collected_data.append({
                    "title": website["title"],
                    "url": url,
                    "search_snippet": website["content"],
                    "relevance_score": website["score"],
                    "navigation_details": navigation_text[:1000],
                    "page_content": page_content[:8000]
                })

                print("Content extracted successfully.")

            except Exception as error:

                print("Website extraction failed:", error)

                collected_data.append({
                    "title": website["title"],
                    "url": url,
                    "error": str(error)
                })

    return collected_data


# --------------------------------
# STEP 4: SAVE RESEARCH DATA
# --------------------------------

def save_research_data(data):

    with open(
        "research_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nResearch data saved successfully!")


# --------------------------------
# MAIN FUNCTION
# --------------------------------

async def main():

    query = input("\nWhat do you want to research? ")

    print("\nSearching the web...")

    search_results = search_web(query)

    print("Search completed.")

    # Validate and remove duplicate URLs
    websites = process_search_results(search_results)

    print("\nUnique websites found:", len(websites))

    # Limit browser research to three websites initially
    websites = websites[:3]

    print("\nStarting browser research...")

    research_data = await research_websites(websites)

    save_research_data(research_data)

    print("\n========== RESEARCH COMPLETED ==========")


if __name__ == "__main__":
    asyncio.run(main())
