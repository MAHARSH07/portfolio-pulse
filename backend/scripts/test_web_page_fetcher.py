from app.web.page_fetcher import WebPageFetcher


def main():
    url = (
        "https://m.economictimes.com/markets/stocks/news/"
        "new-orders-could-put-kpit-tech-on-the-road-to-recovery/"
        "articleshow/134576853.cms"
    )

    fetcher = WebPageFetcher()

    content = fetcher.fetch(url)

    print("Characters:", len(content))
    print()
    print("First 3000 characters:")
    print(content[:3000])


if __name__ == "__main__":
    main()