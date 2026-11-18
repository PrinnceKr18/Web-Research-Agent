
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url):
    """
    Normalize a URL to help identify duplicate links.
    """

    try:
        parsed = urlsplit(url.strip())

        if parsed.scheme not in ("http", "https"):
            return None

        if not parsed.hostname:
            return None

        # Remove URL fragments and normalize hostname
        normalized = urlunsplit((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/") or "/",
            parsed.query,
            ""
        ))

        return normalized

    except ValueError:
        return None


def process_search_results(results):

    processed_results = []
    seen_urls = set()

    for result in results:

        original_url = result.get("url", "")
        clean_url = normalize_url(original_url)

        # Skip invalid URLs
        if clean_url is None:
            continue

        # Skip duplicate URLs
        if clean_url in seen_urls:
            continue

        seen_urls.add(clean_url)

        # Store useful information
        website = {
            "title": result.get("title", "Untitled"),
            "url": clean_url,
            "content": result.get("content", ""),
            "score": result.get("score", 0)
        }

        processed_results.append(website)

    return processed_results


if __name__ == "__main__":

    # Sample Tavily-style search response
    sample_results = [
        {
            "title": "LangChain Introduction",
            "url": "https://example.com/langchain",
            "content": "Introduction to LangChain",
            "score": 0.95
        },
        {
            "title": "LangGraph Guide",
            "url": "https://example.com/langgraph",
            "content": "Introduction to LangGraph",
            "score": 0.90
        },
        {
            "title": "CrewAI Documentation",
            "url": "https://crewai.com/",
            "content": "Introduction to CrewAI",
            "score": 0.88
        },
        {
            "title": "LangChain Introduction Duplicate",
            "url": "https://example.com/langchain",
            "content": "Duplicate result",
            "score": 0.80
        },
        {
            "title": "Python Documentation",
            "url": "https://docs.python.org/",
            "content": "Python documentation",
            "score": 0.85
        }
    ]

    websites = process_search_results(sample_results)

    print("\nCLEAN WEBSITE LIST\n")

    for index, website in enumerate(websites, start=1):

        print(f"Website {index}")
        print("Title:", website["title"])
        print("URL:", website["url"])
        print("Score:", website["score"])
        print("-" * 50)

    print("\nTotal unique websites:", len(websites))
