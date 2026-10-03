from app.ai.agent import get_agent


agent = get_agent()

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "What is the latest news about KPIT Technologies "
                    "and how might it affect my holding?"
                ),
            }
        ]
    }
)

print("\nMessages:\n")

for message in result["messages"]:
    print(f"Type: {type(message).__name__}")
    print(f"Content: {message.content}")
    print(f"Additional kwargs: {message.additional_kwargs}")
    print(f"Response metadata: {message.response_metadata}")

    if getattr(message, "tool_calls", None):
        print("Tool calls:")
        for tool_call in message.tool_calls:
            print(f"  Tool: {tool_call['name']}")
            print(f"  Arguments: {tool_call['args']}")

    print("\n---\n")