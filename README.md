# QnA App (Flask + React)

<p align="center">
  <img src="assets/screen_record.gif" alt="Carousel Demo" height="600"/>
</p>

A Retrieval-Augmented Generation (RAG) Q&A demo using:
- **Backend:** Flask, Python
- **AI:** OpenAI Embeddings & Chat Completions (v1+ client)
- **Frontend:** React + Vite

## Features
1. **/api/ask** (POST): Retrieve relevant contexts, generate an answer.
2. **/api/history** (GET): Fetch past Q&A pairs (in-memory).
3. **/api/summarize** (POST): Summarizer agent refines generated answers.
4. **RAG Retriever:** Embedding-based lookup over `faq.csv`.
5. **Basic styling** with CSS in `public/style.css`.

## Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

## Setup

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # (Windows: .\.venv\Scripts\activate)
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Running

### Start Backend
```bash
python -m backend.main
```

### Start Frontend
```bash
cd frontend
npm run dev
```

Open the browser to http://localhost:5173


## Testing

1. **Unit Test** (`test_retrieval.py`)  
   - Validates that the RAG retriever returns correct FAQ contexts  

2. **Integration Test** (`test_api.py`)  
   - Spins up the Flask app in test mode  
   - Verifies `/api/ask` returns correct JSON schema and status codes  
   - Covers success, missing-parameter, and no-context scenarios

**Run all tests** from the project root:

```bash
pytest
```

## Approach & Comments

- Retrieval: Precompute embeddings for each FAQ entry at startup, perform cosine-sim search on user queries. 
- AI Integration: Two-step multi-agent: 1) answer generation, 2) optional summarization. 
- Tech Choices: Flask for simplicity, React/Vite for fast prototyping, OpenAI Python v1 client. 
- Styling: Lightweight CSS to focus on functionality and demonstrate UI polish.

## Known Limitations & Future Improvements

- In-memory data & history (no persistence). 
- No authentication or rate-limiting. 
- Could add Docker/Docker Compose for full containerization. 
- Potential UI enhancements: confirm contexts (human-in-the-loop), edit before generation.