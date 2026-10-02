from app.ai.tools.web_page import fetch_web_page_tool


def main():
    url = (
        "https://m.economictimes.com/markets/stocks/news/"
        "new-orders-could-put-kpit-tech-on-the-road-to-recovery/"
        "articleshow/134576853.cms"
    )

    result = fetch_web_page_tool.invoke({
        "url": url,
    })

    print("URL:", result["url"])
    print("Characters:", result["character_count"])
    print()
    print("First 3000 characters:")
    print(result["content"][:3000])


if __name__ == "__main__":
    main()