from app.ai.tools.web_research import research_web_tool


def main():
    result = research_web_tool.invoke(
        {
            "query": "KPIT Technologies latest news",
            "topic": "news",
            "days": 7,
        }
    )

    print("Query:", result["query"])
    print("Research results:", len(result["results"]))

    for index, item in enumerate(result["results"], start=1):
        print()
        print(f"{index}. {item['title']}")
        print(f"Source: {item['source']}")
        print(f"URL: {item['url']}")

        if item["content"] is not None:
            print(f"Characters: {len(item['content'])}")
            print("Content preview:")
            print(item["content"][:1000])
        else:
            print("Fetch error:", item["fetch_error"])


if __name__ == "__main__":
    main()