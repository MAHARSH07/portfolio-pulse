from app.ai.agent import get_agent


def main():
    agent = get_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "How much have I invested in total?",
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    print("Agent response:")
    print(final_message.content)


if __name__ == "__main__":
    main()