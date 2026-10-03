from datetime import datetime, timezone

from app.web.schemas import WebSearchResult


# Sources that are generally useful for financial/company research.
PREFERRED_SOURCES = {
    "reuters.com": 5,
    "economictimes.com": 4,
    "m.economictimes.com": 4,
    "moneycontrol.com": 4,
    "business-standard.com": 4,
    "ndtvprofit.com": 4,
    "livemint.com": 4,
}


GENERIC_QUERY_TERMS = {
    "latest",
    "recent",
    "today",
    "news",
    "developments",
    "development",
    "earnings",
    "results",
    "partnerships",
    "partnership",
    "updates",
    "update",
    "stock",
    "share",
    "price",
    "market",
}


def rank_search_results(
    results: list[WebSearchResult],
    query: str,
    topic: str = "general",
) -> list[WebSearchResult]:
    query_words = [
        word.lower()
        for word in query.split()
        if len(word) > 2
    ]

    # -------------------------------------------------------------
    # Identify the company/entity portion of the query.
    #
    # Example:
    #
    # "KPIT Technologies latest news developments earnings"
    #
    # becomes:
    #
    # entity phrase -> "KPIT Technologies"
    #
    # Generic terms such as "latest", "news", and "earnings"
    # are not treated as part of the company name.
    # -------------------------------------------------------------

    entity_words = []

    for word in query_words:
        if word in GENERIC_QUERY_TERMS:
            break

        entity_words.append(word)

    entity_phrase = " ".join(entity_words)

    def score(result: WebSearchResult) -> int:
        score = 0

        title = result.title.lower()
        description = (result.description or "").lower()
        source = (result.source or "").lower()

        searchable_text = f"{title} {description}"

        # ---------------------------------------------------------
        # Strong entity matching
        # ---------------------------------------------------------
        #
        # The complete company/entity phrase is much more important
        # than generic words such as "technologies", "news", etc.
        # ---------------------------------------------------------

        if entity_phrase:
            if entity_phrase in title:
                score += 30

            elif entity_phrase in description:
                score += 15

            else:
                # If the complete entity phrase is absent, check
                # the first entity word separately.
                #
                # For:
                #   "KPIT Technologies"
                #
                # "KPIT" is distinctive, while "Technologies" is
                # generic.
                distinctive_word = entity_words[0]

                if distinctive_word in title:
                    score += 12
                elif distinctive_word in description:
                    score += 6
                else:
                    # The result does not appear to be about the
                    # requested company/entity at all.
                    score -= 30

        # ---------------------------------------------------------
        # General query relevance
        # ---------------------------------------------------------
        #
        # These terms provide only a small contribution.
        # They must never overpower entity relevance.
        # ---------------------------------------------------------

        for term in query_words:
            if term in title:
                score += 1
            elif term in description:
                score += 1

        # ---------------------------------------------------------
        # Source preference
        # ---------------------------------------------------------

        score += PREFERRED_SOURCES.get(source, 0)

        # ---------------------------------------------------------
        # Freshness
        # ---------------------------------------------------------

        if topic == "news" and result.published_at is not None:
            score += 3

            if result.published_at.tzinfo is None:
                published_at = result.published_at.replace(
                    tzinfo=timezone.utc
                )
            else:
                published_at = result.published_at

            age_days = (
                datetime.now(timezone.utc) - published_at
            ).days

            if age_days <= 1:
                score += 5
            elif age_days <= 3:
                score += 3
            elif age_days <= 7:
                score += 1

        return score

    return sorted(
        results,
        key=score,
        reverse=True,
    )