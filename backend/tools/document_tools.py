from langchain_core.tools import tool
from rag.retriever import build_retriever

retriever = build_retriever()

@tool
def query_document(query: str) -> dict:
    """
    Search ONLY within the uploaded PDF document.

    Use this tool ONLY when the user's question is
    specifically about information that may exist in
    the uploaded PDF.

    Do NOT use this tool for:
    - General knowledge
    - Current events
    - Currency conversion
    - Weather
    - Geography
    - Programming help
    - Mathematical calculations

    If the answer is not expected to be in the PDF,
    do not call this tool.
    """

    try:
        result = retriever.invoke(query)
        if not result:
            return {
                'found': False,
                'error': 'No relevant information found in the PDF.'
            }
        context = [doc.page_content for doc in result]
        metadata = [doc.metadata for doc in result]
        return {
            'query': query,
            'context': context,
            'metadata': metadata
        }
    except Exception as e:
        return {
            'found': False,
            'error': f"An error occurred while retrieving information from the PDF: {str(e)}"
        }