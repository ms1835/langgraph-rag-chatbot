from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from graph.state import ChatState
from graph.nodes import create_chat_node

def build_graph(llm_with_tools, tools):
    graph = StateGraph(ChatState)

    graph.add_node('chat_node', create_chat_node(llm_with_tools))

    graph.add_node('tools', ToolNode(tools))

    graph.add_edge(START, 'chat_node')

    graph.add_conditional_edges('chat_node', tools_condition)

    graph.add_edge('tools', 'chat_node')

    return graph.compile(
        checkpointer=InMemorySaver()
    )
