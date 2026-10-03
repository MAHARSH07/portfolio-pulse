from datetime import datetime, timezone

from langchain.agents import create_agent

from app.ai.model import get_llm
from app.ai.prompts.system import SYSTEM_PROMPT
from app.ai.tools.holding import get_holding_tool
from app.ai.tools.portfolio import get_portfolio_tool
from app.ai.tools.web_research import research_web_tool


def get_agent():
    llm = get_llm()

    tools = [
        get_portfolio_tool,
        get_holding_tool,
        research_web_tool,
    ]

    current_date = datetime.now(timezone.utc).date().isoformat()

    runtime_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "Runtime context:\n"
        f"Current date: {current_date}\n"
        "Use this date when interpreting whether retrieved information "
        "is past, current, or future. Do not describe information as "
        "future-dated merely because its year is 2026 or because it "
        "contains a recent date.\n\n"

        "Tool execution priority:\n"
        "When the user asks how recent news may affect a specific holding, "
        "you must obtain both the actual holding data and relevant current "
        "research before answering.\n"
        "The holding data and retrieved research are authoritative inputs "
        "for the final analysis.\n\n"

        "Source attribution:\n"
        "When reporting a material current-news claim, attribute it to "
        "the relevant retrieved source or source type when the source "
        "identity is available. Distinguish company statements, regulatory "
        "filings, news reports, analyst estimates, and PortfolioPulse "
        "calculations.\n"
        "Do not present an analyst's target price, estimate, forecast, "
        "or opinion as PortfolioPulse's own conclusion.\n"
        "Do not present management expectations as established future "
        "outcomes.\n"
        "When multiple sources contain different facts or viewpoints, "
        "keep their attribution separate rather than combining them "
        "into one unsupported conclusion."
    )

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=runtime_system_prompt,
    )