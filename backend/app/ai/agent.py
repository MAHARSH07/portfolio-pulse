from langchain.agents import create_agent

from app.ai.model import get_llm
from app.ai.tools.portfolio import get_portfolio_tool
from app.ai.tools.holding import get_holding_tool
from app.ai.tools.web_search import search_web_tool
from app.ai.prompts.system import SYSTEM_PROMPT


def get_agent():
    llm = get_llm()

    tools = [
        get_portfolio_tool,
        get_holding_tool,
        search_web_tool,
    ]

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
