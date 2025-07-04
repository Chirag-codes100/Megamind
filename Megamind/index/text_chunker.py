import re

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits a large string into chunks of chunk_size (with optional overlap).
    Returns a list of chunk strings.
    """
    words = text.split()
    chunks = []
    for start in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[start:start+chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks

def pdf_to_chunks(pages_dict, chunk_size=500, overlap=50):
    """
    Takes {page_number: text} and returns list of {page, chunk_id, text}.
    """
    all_chunks = []
    for page, text in pages_dict.items():
        if not text:
            continue
        page_chunks = chunk_text(text, chunk_size, overlap)
        for idx, chunk in enumerate(page_chunks, 1):
            all_chunks.append({"page": page, "chunk_id": idx, "text": chunk})
    return all_chunks

if __name__ == "__main__":
    # Simple test
    pages_dict = {
        1: "This is some long text that should be chunked. " * 50,
        2: "Page two is here. " * 40
    }
    chunks = pdf_to_chunks(pages_dict)
    for c in chunks:
        print(f"Page {c['page']} Chunk {c['chunk_id']}: {c['text'][:60]}...")
