from app.ai.tools.portfolio import get_portfolio_tool


def main():
    result = get_portfolio_tool.invoke({})

    print("Portfolio tool result:")
    print(result)


if __name__ == "__main__":
    main()