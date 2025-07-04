import streamlit as st
import os
import base64

from Megamind.highlight.pdf_highlight import highlight_pdf
from Megamind.highlight.highlight_ppt import export_slide_as_image
from megamind_backend import megamind_answer

st.set_page_config(page_title="Megamind QnA", page_icon="🧠", layout="wide")

# --- HEADER AND SIDEBAR ---
st.markdown("""
    <style>
        .block-container {padding-top: 2rem;}
        .big-title {font-size:3rem; color:#E32227; font-weight:900; letter-spacing:2px;}
        .subtitle {font-size:1.4rem; color:#4F8BF9;}
        body {
            background: linear-gradient(90deg,#FFF9F4,#ffeaea 40%,#ffeaea 100%);
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    st.header("🌈 About Megamind")
    st.write("Ask anything from PDFs, PPTX, images, YouTube or websites!")
    st.info("Your Personal Helper at Your Service")
    st.success("Pro tip: Use color in your docs for best results!")

# --- MAIN UI LAYOUT ---
col1, col2 = st.columns([2, 2])
with col1:
    st.markdown("<div class='big-title'>🧠 Megamind Universal QnA Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your Personal Document & Media Genius!</div>", unsafe_allow_html=True)
    source_type = st.radio(
        "Select Source Type:",
        ("PDF", "PPTX", "Image", "YouTube Link", "Website URL"),
        horizontal=True
    )
    uploaded_file = None
    url_input = None

    if source_type in ["PDF", "PPTX", "Image"]:
        uploaded_file = st.file_uploader(f"Upload your {source_type} file", type=["pdf", "pptx", "png", "jpg", "jpeg", "bmp"])
    elif source_type == "YouTube Link":
        url_input = st.text_input("Paste YouTube video link:")
    elif source_type == "Website URL":
        url_input = st.text_input("Paste website URL:")

    question = st.text_input("Ask your question (MCQ or open-ended):")

    get_answer = st.button("🪄 Get Answer")

with col2:
    # Placeholder for showing answer and document side-by-side
    result_placeholder = st.empty()
    doc_placeholder = st.empty()
    download_placeholder = st.empty()

if get_answer:
    with st.spinner("Megamind is thinking..."):
        file_path = None
        if uploaded_file:
            if not os.path.exists("temp"):
                os.makedirs("temp")
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        answer, filetype, page_num, raw_transcript = megamind_answer(
            source_type,
            file_path=file_path,
            url_input=url_input,
            question=question
        )

        # ---- DISPLAY LOGIC ----
        with col1:
            if filetype == "pdf" and file_path and answer and page_num:
                highlighted_pdf_path = os.path.join("temp", "highlighted.pdf")
                highlighted = highlight_pdf(file_path, highlighted_pdf_path, answer, page_num)
                with open(highlighted_pdf_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="420" height="600" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                if not highlighted:
                    st.warning("Highlight could not be shown (text not found on this page, or scanned PDF).")
            elif filetype == "pptx" and file_path and answer and page_num:
                highlighted_slide_image = os.path.join("temp", "highlighted_slide.png")
                export_slide_as_image(file_path, page_num, highlighted_slide_image)
                st.image(highlighted_slide_image, caption=f"Highlighted Slide {page_num}", use_column_width=True)
            # Add other types (images, YouTube) as you expand
        with col2:
            if answer:
                st.success("AI Answer: " + str(answer))
                # --- YouTube Timestamped Link ---
                if filetype == "youtube" and raw_transcript:
                    timestamp = None
                    # Try to find the chunk that matches the answer
                    if page_num and page_num - 1 < len(raw_transcript):
                        entry = raw_transcript[page_num - 1]
                        timestamp = int(entry['start'])
                    if not timestamp and answer:
                        # Fuzzy match in transcript
                        for entry in raw_transcript:
                            if answer.lower()[:30] in entry['text'].lower():
                                timestamp = int(entry['start'])
                                break
                    if timestamp and url_input:
                        import re

                        match = re.search(r'(?:v=|youtu\.be/|embed/)([\w-]+)', url_input)
                        video_id = match.group(1) if match else ""
                        yt_link = f"https://www.youtube.com/watch?v={video_id}&t={timestamp}s"
                        st.markdown(f"🔗 [Jump to answer in YouTube video]({yt_link})", unsafe_allow_html=True)
                    elif url_input:
                        st.markdown(f"🔗 [Open the YouTube video]({url_input})", unsafe_allow_html=True)

                if filetype == "pdf" and file_path and page_num:
                    st.download_button("Download Highlighted PDF", open(highlighted_pdf_path, "rb"), file_name="highlighted.pdf")
                elif filetype == "pptx" and file_path and page_num:
                    st.download_button("Download Slide Image", open(highlighted_slide_image, "rb"), file_name="highlighted_slide.png")
            else:
                st.error("Sorry, no answer could be found.")

