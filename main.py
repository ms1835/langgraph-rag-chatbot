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

        response = chatbot.invoke(
            {
                'messages': [
                    HumanMessage(
                        content= user_prompt
                    )
                ]
            },
            config=config
        )
        print("AI: ", response['messages'][-1].content)
    except KeyboardInterrupt:
        print("\nExiting chat...")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")