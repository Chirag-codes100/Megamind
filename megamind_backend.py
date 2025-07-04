import os
from Megamind.ingest.url_ingest import extract_text_from_url
from Megamind.ingest.ppt_ingest import extract_ppt_text_by_slide
from Megamind.ingest.youtube_ingest import extract_transcript
from Megamind.ingest.image_ingest import extract_text_from_image
from Megamind.ingest.pdf_ingest import extract_pdf_text_by_page
from Megamind.index.text_chunker import pdf_to_chunks
from Megamind.index.keyword_search import keyword_search
from Megamind.qa.gemini_qa import ask_gemini

from Megamind.highlight.parse_answer import extract_text_and_page
from Megamind.utils.pdf_open import open_pdf_at_page

def megamind_answer(source_type, file_path=None, url_input=None, question=None):
    raw_transcript = None
    if source_type == "PDF":
        pages = extract_pdf_text_by_page(file_path)
        filetype = "pdf"
    elif source_type == "PPTX":
        pages = extract_ppt_text_by_slide(file_path)
        filetype = "pptx"
    elif source_type == "Image":
        img_text = extract_text_from_image(file_path)
        pages = {1: img_text}
        filetype = "image"
    elif source_type == "YouTube Link":
        pages, raw_transcript = extract_transcript(url_input)
        filetype = "youtube"
    elif source_type == "Website URL":
        url_text = extract_text_from_url(url_input)
        pages = {1: url_text}
        filetype = "url"
    else:
        return "Unsupported source type.", None, None, None

    all_chunks = pdf_to_chunks(pages)
    top_chunks = keyword_search(all_chunks, question, top_n=3)
    answer = ask_gemini(question, top_chunks)
    answer_text, page_num = extract_text_and_page(answer)
    return answer, filetype, page_num, raw_transcript if filetype == "youtube" else None

