import pytest
from backend.retrieval import get_contexts

@pytest.mark.parametrize("q,expected", [
    ("What is this QnA App?", ["The QnA App is a RAG-powered question-and-answer service combining embedding-based retrieval with AI-generated responses."]),
    ("Which AI models are used?", ["We use the OpenAI text-embedding-ada-002 model for embeddings and gpt-4o for answer generation and summarization."])
])
def test_retrieval(q, expected):
    """
    Check functionality of retrieval.
    """
    results = get_contexts(q)
    assert expected[0] in results

def test_retrieval_empty_query_yields_empty_list():
    """
    If the query is empty or whitespace, retrieval should return an empty list.
    """
    contexts = get_contexts("   ")
    assert contexts == [], "Expected no contexts for an empty query"