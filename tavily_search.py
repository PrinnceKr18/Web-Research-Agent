
from tavily import TavilyClient


def search_web(query):

    # Create Tavily client in keyless mode
    client = TavilyClient()

    # Search the web
    response = client.search(
        query=query,
        max_results=5
    )

    return response


if __name__ == "__main__":

    query = input("What do you want to search? ")

    results = search_web(query)

    print("\n========== SEARCH RESULTS ==========\n")

    for index, result in enumerate(results["results"], start=1):

        print(f"\nResult {index}")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Content:", result["content"])
        print("Relevance Score:", result["score"])

        print("-" * 60)
