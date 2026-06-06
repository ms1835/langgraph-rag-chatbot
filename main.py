from chatbot.chatbot import chatbot
from langchain_core.messages import HumanMessage

config = {
    "configurable": {
        "thread_id": "1"
    }
}

while True:
    try:
        user_prompt = input("User: ")

        if(user_prompt.strip().lower() in ['exit', 'bye', 'quit']):
            print("Goodbye!")
            break

        for msg, meta in chatbot.stream(
            {
                "messages": [
                    HumanMessage(content=user_prompt)
                ]
            },
            config=config,
            stream_mode="messages"
        ):
            if (
                meta.get("langgraph_node") == "chat_node"
                and msg.content
            ):
                print(msg.content, end="", flush=True)

        print()

    except KeyboardInterrupt:
        print("\nExiting chat...")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")