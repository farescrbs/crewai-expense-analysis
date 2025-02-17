from needle.v1 import NeedleClient
from crewai.tools import tool

@tool("Search Knowledge Base")
def search_knowledge_base(query: str) -> str:
    """
    Retrieve information from your knowledge base containing unstructured data such as
    invoices, reports, emails, and more.
    
    Args:
        query (str): The search query to find relevant invoice data.
    """
    ndl = NeedleClient()
    return ndl.collections.search(
        collection_id="clt_01JKBAHP3419YYWZ7CQJ59S60N",  # Replace with your actual collection ID
        text=query,
        top_k=20,
    )