from fastapi import APIRouter, HTTPException

from app.ai.service import AIService
from app.schemas.ai import ChatRequest, ChatResponse
from app.ai.service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        service = AIService()

        response = service.chat(request.message)

        return ChatResponse(response=response)

    except Exception as exc:
        print(f"AI generation error: {exc}")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate AI response.",
        ) from exc