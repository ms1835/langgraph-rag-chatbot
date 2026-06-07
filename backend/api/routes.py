import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage

from chatbot.chatbot import chatbot

from api.schemas import ChatRequest

router = APIRouter()


def _extract_streamed_text(event):
    if event["event"] not in {"on_chat_model_stream", "on_chain_stream"}:
        return None

    if event["event"] == "on_chain_stream" and event.get("name") != "chat_node":
        return None

    chunk = event["data"].get("chunk")
    if chunk is None:
        return None

    # Try to extract content from chunk (handles various LangChain message types)
    if hasattr(chunk, "content"):
        content = getattr(chunk, "content")
        if content:
            return content

    if isinstance(chunk, dict):
        if "content" in chunk:
            return chunk["content"]

        # Handle graph/chain chunks with messages list
        if "messages" in chunk:
            messages = chunk.get("messages")
            if isinstance(messages, list) and messages:
                first = messages[0]
                
                # If it's a message object with content attribute
                if hasattr(first, "content"):
                    return getattr(first, "content")
                
                # If it's a string representation of a message
                if isinstance(first, str):
                    # Extract content from string like: content="text" attr=...
                    for quote_char in ['"', "'"]:
                        pattern = f'content={quote_char}'
                        if pattern in first:
                            start = first.find(pattern) + len(pattern)
                            end = first.find(quote_char, start)
                            if end != -1 and end > start:
                                return first[start:end]

    return None


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
            content = _extract_streamed_text(event)
            if content:
                token_payload = {
                    "type": "token",
                    "content": content,
                }
                yield f"data: {json.dumps(token_payload)}\n\n"
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )