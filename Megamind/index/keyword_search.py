import re

def keyword_search(chunks, question, top_n=3):
    """
    Simple keyword-based retrieval. Finds chunks with the most question word matches.
    """
    question_words = set(re.findall(r'\w+', question.lower()))
    scored = []
    for chunk in chunks:
        text_words = set(re.findall(r'\w+', chunk['text'].lower()))
        common = question_words & text_words
        score = len(common)
        scored.append((score, chunk))
    scored.sort(reverse=True, key=lambda x: x[0])
    # Filter zero-score chunks if possible
    return [c for s, c in scored if s > 0][:top_n] or [scored[0][1]]  # Always return at least one
