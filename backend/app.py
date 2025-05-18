"""
Flask application for QnA RAG service.
Endpoints to ask questions, view history, and summarize answers.
"""
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from backend.retrieval import get_contexts
from backend.ai_client import generate_answer, summarize_answer


app = Flask(__name__)
# Enable CORS for React dev-server
CORS(app, origins=["http://localhost:5173"])

# In-memory history log for Q&A pairs
history_log = []

@app.route('/api/ask', methods=['POST'])
def ask():
    """
    POST /api/ask
    Body JSON: { "question": "..." }
    Returns: { question, contexts[], answer }
    """
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    if not question:
        abort(400, description="Missing 'question' in request body")

    # Retrieve top contexts via RAG
    contexts = get_contexts(question)
    app.logger.debug("Retrieved contexts: %s", contexts)
    if not contexts:
        abort(404, description="No relevant context found")

    # Generate the AI answer
    answer = generate_answer(question, contexts)

    # Append to history log
    history_log.append({"question": question, "answer": answer})

    return jsonify({
        'question': question,
        'contexts': contexts,
        'answer': answer
    })

"""
Not using this endpoint since history is working only for one session, and is currently implemented in frontend 
using react state, maybe will use it if I'll implement persistent history in the future.
"""
@app.route('/api/history', methods=['GET'])
def get_history():
    """
    GET /api/history
    Returns JSON array of past Q&A pairs.
    """
    return jsonify(history_log)

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    POST /api/summarize
    Body JSON: { "answer": "..." }
    Returns: { summary: "..." }
    """
    data = request.get_json() or {}
    answer = data.get('answer', '').strip()
    if not answer:
        abort(400, description="Missing 'answer' in request body")

    # Use multi-agent summarizer
    summary = summarize_answer(answer)
    return jsonify({'summary': summary})
