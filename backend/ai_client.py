"""
AI client: wrapper for OpenAI chat and summarization calls.
Defining two agents: answer generator and summarizer.
"""
from openai import OpenAI, APIError, APITimeoutError, BadRequestError


client = OpenAI(api_key="API_KEY")

SYSTEM_PROMPT = (
    "You are an AI assistant. Use the provided contexts to answer concisely. "
    "If the context does not contain the answer, respond with 'I don't know.'"
)


def generate_answer(question: str, contexts: list[str]) -> str:
    """
    Generate an AI answer by combining system prompt, contexts, and user question.
    Returns the assistant's answer text.
    """
    # Build the user message including retrieved contexts
    user_message = (
        "Contexts:\n" + "\n".join(f"- {c}" for c in contexts) +
        f"\n\nQuestion: {question}\nAnswer:"
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=256,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except (APIError, APITimeoutError, BadRequestError) as e:
        return f"Error generating answer: {str(e)}"


def summarize_answer(answer: str) -> str:
    """
    Summarize the provided answer to be more concise and clear.
    Demonstrates a secondary "summarizer agent" for multi-agent workflows.
    """
    summary_prompt = (
        "You are a summarization agent. "
        "Please provide a concise summary of the following answer:\n\n" + answer
    )
    messages = [
        {"role": "system", "content": "You summarize AI-generated answers."},
        {"role": "user", "content": summary_prompt}
    ]
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=128,
            temperature=0.1,
        )
        return resp.choices[0].message.content.strip()
    except (APIError, APITimeoutError, BadRequestError) as e:
        return f"Error summarizing answer: {str(e)}"