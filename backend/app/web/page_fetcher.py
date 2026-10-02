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

        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
            ]
        ):
            element.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text