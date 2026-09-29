from langchain.agents import create_agent

from app.ai.model import get_llm
from app.ai.tools.portfolio import get_portfolio_tool


def get_agent():
    llm = get_llm()

    tools = [
        get_portfolio_tool,
    ]

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are PortfolioPulse, an AI investment portfolio assistant. "
            "You have access to the user's current portfolio through tools. "
            "Use the portfolio tool whenever the user's question requires "
            "current portfolio information. "
            "Do not invent portfolio values or holdings. "
            "When portfolio prices are marked as DELAYED, make that clear "
            "when relevant."
        ),
    )