import google.generativeai as genai
from config import API_KEY
genai.configure(api_key=API_KEY)


def ask_gemini(question, context_chunks):
    context = ""
    for c in context_chunks:
        context += f"(Page {c['page']}): {c['text']}\n"
    prompt = (
        "Answer the question using only the text below. "
        "If not found, say 'Not found in document.'\n"
        f"{context}\n"
        f"QUESTION: {question}\n"
        "Include the quote and page number."
    )
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt])
    return response.text

# Example quick test
if __name__ == "__main__":
    chunks = [{'page': 1, 'text': 'Gemini is an AI developed by Google.'}]
    question = "What is Gemini?"
    print(ask_gemini(question, chunks))
