import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage

from chatbot.chatbot import chatbot

from api.schemas import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    async def event_generator():
        async for event in chatbot.astream_events(
            {
                "messages": [
                    HumanMessage(
                        content=request.message
                    )
                ]
            },
            config=config,
            version="v2"
        ):
            # print(f"Generated event: {event}")
        #     yield (
        #         f"data: {json.dumps(event)}\n\n"
        # )
            if (
                event["event"] == "on_chat_model_stream"
            ):
                chunk = event["data"]["chunk"]
                if chunk.content:
                    token_payload = {
                        "type": "token",
                        "content": chunk.content,
                    }
                    yield (
                        f"data: {json.dumps(token_payload)}\n\n"
                    )
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )