import streamlit as st
import os

st.set_page_config(page_title="Megamind QnA", page_icon="🧠")

st.title("🧠 Megamind Universal QnA Assistant")

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

if st.button("Get Answer"):
    with st.spinner("Processing..."):
        # Save uploaded file to temp dir if present
        file_path = None
        if uploaded_file:
            if not os.path.exists("temp"):
                os.makedirs("temp")
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        # Here you will call your Megamind pipeline (backend)
        st.success("This is where your real answer will appear. (Integration coming next!)")
