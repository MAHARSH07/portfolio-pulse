from app.web.providers.factory import get_web_search_provider


def main():
    provider = get_web_search_provider()

    print("Provider:", type(provider).__name__)


if __name__ == "__main__":
    main()