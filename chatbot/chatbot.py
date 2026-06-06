from llm.groq_client import get_llm
from tools.math_tools import (
    add,
    subtract,
    multiply,
    divide,
    square,
    modulo
)
from tools.document_tools import query_document
from graph.workflow import build_graph

tools = [
    query_document,
    add,
    subtract,
    multiply,
    divide,
    modulo,
    square
]

llm = get_llm()
llm_with_tools = llm.bind_tools(tools)

chatbot = build_graph(llm_with_tools, tools)
