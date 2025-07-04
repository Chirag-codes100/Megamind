import fitz  # PyMuPDF

def highlight_pdf(input_pdf, output_pdf, text, page_number):
    doc = fitz.open(input_pdf)
    page = doc[page_number-1]
    found = False

    # Try both the whole answer and a shorter phrase
    search_texts = [text.strip().replace('\n', ' ')]
    if len(search_texts[0]) > 40:
        # Also try first 5 words as backup
        short = " ".join(search_texts[0].split()[:5])
        if short not in search_texts:
            search_texts.append(short)

    for search_text in search_texts:
        for inst in page.search_for(search_text):
            annot = page.add_highlight_annot(inst)
            annot.set_colors(stroke=(1, 0, 0))  # Bright red
            annot.update()
            found = True

    doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    doc.close()
    return found
