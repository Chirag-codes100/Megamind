import sys
import os
import webbrowser
import urllib.parse
from Megamind.highlight.parse_answer import extract_text_and_page
from Megamind.ingest.url_ingest import extract_text_from_url
from Megamind.utils.pdf_open import open_pdf_at_page
from Megamind.ingest.ppt_ingest import extract_ppt_text_by_slide
from Megamind.ingest.youtube_ingest import extract_transcript
from Megamind.ingest.image_ingest import extract_text_from_image
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingest.pdf_ingest import extract_pdf_text_by_page
from index.text_chunker import pdf_to_chunks
from index.keyword_search import keyword_search
from qa.gemini_qa import ask_gemini

def generate_text_fragment_link(url, answer_text):
    snippet = answer_text.strip().replace('\n', ' ')
    encoded = urllib.parse.quote(snippet)
    return f"{url}#:~:text={encoded}"

def main():
    print("Welcome to Megamind!")
    file_or_url = input("Enter path to your PDF, PPTX, image, YouTube, or a URL: ").strip().strip('"').strip("'")
    pages = None
    filetype = None
    raw_transcript = None  # for YouTube

    if file_or_url.startswith("http://") or file_or_url.startswith("https://"):
        # Detect YouTube
        if ("youtube.com/watch" in file_or_url) or ("youtu.be/" in file_or_url):
            pages, raw_transcript = extract_transcript(file_or_url)
            filetype = "youtube"
        else:
            url_text = extract_text_from_url(file_or_url)
            pages = {1: url_text}
            filetype = "url"
    else:
        if not os.path.isfile(file_or_url):
            print("File not found!")
            return
        ext = os.path.splitext(file_or_url)[-1].lower()
        if ext == ".pdf":
            pages = extract_pdf_text_by_page(file_or_url)
            filetype = "pdf"
        elif ext == ".pptx":
            pages = extract_ppt_text_by_slide(file_or_url)
            filetype = "pptx"
        elif ext in [".png", ".jpg", ".jpeg", ".bmp"]:
            img_text = extract_text_from_image(file_or_url)
            pages = {1: img_text}
            filetype = "image"
        else:
            print("Unsupported file type!")
            return

    all_chunks = pdf_to_chunks(pages)
    print(f"Extracted and chunked {len(all_chunks)} text blocks.")

    while True:
        question = input("\nAsk a question (or type 'exit' to quit): ").strip()
        if question.lower() in ['exit', 'quit']:
            break
        top_chunks = keyword_search(all_chunks, question, top_n=3)
        answer = ask_gemini(question, top_chunks)
        print("\n--- Megamind Answer ---")
        print(answer)
        answer_text, page_num = extract_text_and_page(answer)

        if filetype == "url":
            print(f"(This answer is from the provided URL)")
            found = False
            for chunk in top_chunks:
                if answer_text and answer_text.lower() in chunk['text'].lower():
                    idx = chunk['text'].lower().find(answer_text.lower())
                    start = max(0, idx - 40)
                    end = min(len(chunk['text']), idx + len(answer_text) + 40)
                    print("\nContext Snippet:")
                    print("...", chunk['text'][start:end], "...")
                    found = True
                    break
            if not found:
                print(all_chunks[0]['text'][:300])
            if answer_text:
                highlight_url = generate_text_fragment_link(file_or_url, answer_text)
                print(f"\n🔗 Click to jump & highlight in Chrome/Edge:\n{highlight_url}\n")
                webbrowser.open(highlight_url)
            else:
                webbrowser.open(file_or_url)

        elif filetype == "youtube":
            print(f"(This answer is from the YouTube transcript)")
            timestamp = None
            if page_num:
                if page_num in pages:
                    ts_match = pages[page_num][:7]  # e.g., '[01:15]'
                    timestamp = ts_match.strip('[]')
            else:
                for entry in raw_transcript:
                    if answer_text and answer_text.lower() in entry['text'].lower():
                        time = int(entry['start'])
                        mins = time // 60
                        secs = time % 60
                        timestamp = f"{mins:02d}:{secs:02d}"
                        break
            if timestamp:
                import re
                match = re.search(r'(?:v=|youtu\.be/|embed/)([\w-]+)', file_or_url)
                video_id = match.group(1) if match else None
                if video_id:
                    ts_seconds = int(timestamp.split(':')[0]) * 60 + int(timestamp.split(':')[1])
                    jump_url = f"https://www.youtube.com/watch?v={video_id}&t={ts_seconds}s"
                    print(f"\n🔗 Click to jump to timestamp:\n{jump_url}\n")
                    webbrowser.open(jump_url)
            else:
                webbrowser.open(file_or_url)

        elif filetype == "pdf":
            if page_num:
                open_pdf_at_page(file_or_url, page_num)
                print(f"(PDF opened at page {page_num} in your browser)")
            else:
                print("Could not parse page number from answer.")

        elif filetype == "pptx":
            if page_num:
                print(f"(This answer is from Slide {page_num})")
                print("\nSlide Preview:")
                print(pages[page_num][:300])  # Show first 300 chars from that slide
            else:
                print("Could not parse slide number from answer.")

        elif filetype == "image":
            print(f"(This answer is from the provided image)")
            print("\nContext Snippet:\n")
            print(pages[1][:300])  # Show snippet

        else:
            print("Could not parse page/slide number from answer.")

if __name__ == "__main__":
    main()
