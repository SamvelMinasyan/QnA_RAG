import pytest
import html
from backend.app import app as flask_app


@pytest.fixture
def client():
    """Create a Flask test client for sending HTTP requests."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_ask_endpoint_returns_200_for_valid_question(client):
    """
    POST /api/ask with a valid question should:
      - return HTTP 200
      - return JSON with keys: 'question', 'contexts', 'answer'
      - echo back the same question
      - include a non-empty list of contexts
      - include a non-empty answer string
    """
    response = client.post(
        "/api/ask",
        json={"question": "What future features are planned?"}
    )
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    data = response.get_json()
    # Check that all expected keys are present
    assert set(data.keys()) == {"question", "contexts", "answer"}
    # The question should be echoed verbatim
    assert data["question"] == "What future features are planned?"
    # Contexts must be a list with at least one entry
    assert isinstance(data["contexts"], list) and len(data["contexts"]) > 0
    # Answer must be a non-empty string
    assert isinstance(data["answer"], str) and data["answer"].strip(), "Answer should be non-empty"


def test_ask_endpoint_handles_missing_question(client):
    """
    POST /api/ask without a 'question' field should:
      - return HTTP 400 Bad Request
      - include a message about the missing 'question'
    """
    response = client.post("/api/ask", json={})
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"

    body = response.get_data(as_text=True)
    unescaped = html.unescape(body) # making html readable
    assert "Missing 'question' in request body" in unescaped, (
        f"Expected missing-question error message, got:\n{unescaped}"
    )


def test_ask_endpoint_handles_no_context_found(client, monkeypatch):
    """
    If the retrieval layer returns no contexts, the endpoint should:
      - return HTTP 404 Not Found
    We monkeypatch `get_contexts` in the app module to force an empty result.
    """
    import backend.app as app_module

    # Monkeypatch the function used by the /api/ask handler
    monkeypatch.setattr(app_module, "get_contexts", lambda q: [])

    response = client.post(
        "/api/ask",
        json={"question": "Something completely unrelated"}
    )
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"
