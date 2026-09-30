from app.ai.tools.holding import get_holding_tool


def main():
    result = get_holding_tool.invoke(
        {
            "symbol": "KPITTECH",
        }
    )

    print("Holding tool result:")
    print(result)


if __name__ == "__main__":
    main()