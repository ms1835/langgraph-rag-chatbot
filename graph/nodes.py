from langchain_core.messages import SystemMessage, AIMessage
from prompts.system_prompt import SYSTEM_PROMPT
from graph.state import ChatState

def create_chat_node(llm_with_tools):

    def chat_node(state: ChatState):
        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                *state['messages']
            ]
            response = llm_with_tools.invoke(messages)

            # print("\n=== LLM RESPONSE ===")
            # print(response)
            # print("====================\n")

            return {'messages': [response]}
        
        except Exception as e:
            return {
                "messages": [
                    AIMessage(
                        content="Sorry, I encountered an error while processing your request."
                    )
                ]
            }
    return chat_node