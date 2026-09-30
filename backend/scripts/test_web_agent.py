from app.ai.agent import get_agent


def main():
    agent = get_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What's the latest news about KPIT Technologies?",
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    print("Agent response:")
    print(final_message.content)


if __name__ == "__main__":
    main()