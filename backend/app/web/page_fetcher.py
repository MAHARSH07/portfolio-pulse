import httpx
from bs4 import BeautifulSoup


class WebPageFetcher:
    def fetch(self, url: str) -> str:
        response = httpx.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/154.0.0.0 Safari/537.36"
                )
            },
            timeout=20.0,
            follow_redirects=True,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that normally do not contain article content.
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
                "aside",
                "form",
                "iframe",
            ]
        ):
            element.decompose()

        # Remove common advertisement and recommendation containers.
        noisy_keywords = [
            "advertisement",
            "ad-container",
            "ad-wrapper",
            "ads",
            "banner",
            "popup",
            "modal",
            "newsletter",
            "recommended",
            "related",
            "trending",
            "sponsored",
            "social-share",
        ]

        for element in soup.find_all(["div", "section", "aside"]):
            if not element.attrs:
                continue

            element_id = element.get("id") or ""
            element_classes = element.get("class") or []

            attributes = " ".join(
                [
                    str(element_id),
                    " ".join(str(value) for value in element_classes),
                ]
            ).lower()

            if any(
                keyword in attributes
                for keyword in noisy_keywords
            ):
                element.decompose()

        # Prefer semantic article containers.
        article = soup.find("article")

        if article is None:
            article = soup.find("main")

        if article is None:
            article = soup.find(
                attrs={
                    "itemprop": "articleBody",
                }
            )

        if article is None:
            article = soup

        text = article.get_text(
            separator=" ",
            strip=True,
        )

        return text