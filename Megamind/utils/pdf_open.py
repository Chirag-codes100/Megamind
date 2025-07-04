import os

def open_pdf_at_page(pdf_path, page_num):
    abs_path = os.path.abspath(pdf_path)
    pdf_url = f"file:///{abs_path.replace(os.sep, '/')}"
    cmd = f'start chrome "{pdf_url}#page={page_num}"'
    os.system(cmd)
