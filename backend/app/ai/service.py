import json

from app.ai.agent import get_agent
from app.ai.model import get_llm


class AIService:
    def __init__(self):
        self.agent = get_agent()
        self.llm = get_llm()

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

        messages = result["messages"]

        holding_data = None
        research_data = None

        for msg in messages:
            tool_name = getattr(msg, "name", None)
            content = getattr(msg, "content", None)

            if not content:
                continue

            if tool_name == "get_holding_tool":
                holding_data = self._parse_tool_content(content)

            elif tool_name == "research_web_tool":
                research_data = self._parse_tool_content(content)

        # If this was not a holding + research question,
        # return the normal agent response directly.
        if holding_data is None or research_data is None:
            final_message = messages[-1]
            return final_message.content

        return self._synthesize_response(
            user_question=message,
            holding_data=holding_data,
            research_data=research_data,
        )

    @staticmethod
    def _parse_tool_content(content):
        if isinstance(content, dict):
            return content

        if isinstance(content, str):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content

        return content

    def _synthesize_response(
        self,
        user_question: str,
        holding_data,
        research_data,
    ) -> str:
        synthesis_prompt = f"""
            You are the final response writer for PortfolioPulse.

            Answer the user's question directly using ONLY the supplied portfolio
            data and retrieved research for current factual claims.

            USER QUESTION:
            {user_question}

            ACTUAL HOLDING DATA:
            {json.dumps(holding_data, indent=2, default=str)}

            RETRIEVED WEB RESEARCH:
            {json.dumps(research_data, indent=2, default=str)}

            IMPORTANT INSTRUCTIONS:

            1. If the user asks how news may affect their holding, you MUST explicitly
            connect the retrieved developments to the actual holding data.

            2. Start with the user's actual holding context when relevant:
            - quantity
            - average price
            - current price
            - current value
            - profit/loss
            - profit/loss percentage
            Use only values supplied above.

            3. Clearly distinguish:
            - reported facts from the research
            - your interpretation of what those facts could mean
            - uncertainty about future stock-price movement

            4. For each important development, explain whether it could represent a
            potential positive factor, negative factor, mixed factor, or uncertainty,
            but only when the retrieved evidence supports that interpretation.

            5. Do not invent company facts, financial metrics, targets, catalysts,
            risks, guidance, or future outcomes.

            6. If an analyst provides a target price or forecast, identify it as an
            analyst estimate. Do not present it as PortfolioPulse's prediction.

            7. If the portfolio price source is DELAYED, explicitly say so.

            8. Do not automatically recommend buying, selling, holding, averaging, or
            exiting the position unless the user explicitly asks for such a decision.

            9. Do not claim that the news definitely caused a stock-price movement
            unless the retrieved research explicitly establishes that connection.

            10. Prefer a concise structure:

            ## Your Holding
            Briefly describe the actual position.

            ## Latest Relevant Developments
            Summarize only the developments relevant to the question.

            ## Potential Impact on Your Holding
            Connect those developments specifically to the user's position.
            Separate positive, negative, mixed, and uncertain factors where supported.

            ## What to Watch
            Mention only upcoming events or factors supported by the retrieved
            research.

            11. Do not repeat a generic company profile.

            12. Do not manufacture additional developments just to make the answer
            look comprehensive.

            13. Use ₹/INR for portfolio monetary values. Preserve USD only when the
            retrieved research explicitly reports a USD-denominated company metric.

            14. When citing research in prose, identify the source by its supplied
            source name when available.

            Now produce the final answer.
            """

        response = self.llm.invoke(synthesis_prompt)

        print("\n[AI SYNTHESIS] Response type:", type(response).__name__)
        print("[AI SYNTHESIS] Response length:", len(response.content))
        print("[AI SYNTHESIS] Full response:")
        print(response.content)
        print("[AI SYNTHESIS] END RESPONSE\n")

        return response.content
