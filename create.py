import os

folders = [
    'Megamind/ingest',
    'Megamind/ocr',
    'Megamind/index',
    'Megamind/qa',
    'Megamind/highlight',
    'Megamind/cli',
    'Megamind/data'
]

files = [
    'Megamind/ingest/pdf_ingest.py',
    'Megamind/ocr/ocr_utils.py',
    'Megamind/index/vector_store.py',
    'Megamind/qa/gemini_qa.py',
    'Megamind/highlight/pdf_highlight.py',
    'Megamind/cli/main.py',
    'Megamind/requirements.txt',
    'Megamind/README.md'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    open(file, 'a').close()  # Create empty files

print("Project structure created!")
