from app.ai.agent import get_agent


class AIService:

    def __init__(self):
        self.agent = get_agent()

    def chat(self, message: str) -> str:
        result = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            }
        )

        final_message = result["messages"][-1]

        return final_message.content