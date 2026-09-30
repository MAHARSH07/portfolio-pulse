from app.web.providers.tavily import TavilySearchProvider
from app.web.service import WebSearchService

def main():
    provider = TavilySearchProvider()
    service = WebSearchService(provider)

    result = service.search("KPIT Technologies latest news")

    print(f"Query: {result.query}")
    print(f"Results: {len(result.results)}")

    for index, item in enumerate(result.results, start=1):
        print()
        print(f"{index}. {item.title}")
        print(f"   Source: {item.source}")
        print(f"   URL: {item.url}")
        print(f"   Description: {item.description}")


if __name__ == "__main__":
    main()