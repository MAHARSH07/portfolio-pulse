from app.ai.tools.web_search import search_web_tool


def main():
    result = search_web_tool.invoke(
        {
            "query": "KPIT Technologies",
            "topic": "news",
            "days": 7,
        }
    )

    print(f"Query: {result['query']}")
    print(f"Results: {len(result['results'])}")

    for index, item in enumerate(result["results"], start=1):
        print()
        print(f"{index}. {item['title']}")
        print(f"   Source: {item['source']}")
        print(f"   URL: {item['url']}")
        print(f"   Description: {item['description']}")


if __name__ == "__main__":
    main()
