from PIL import Image
import pytesseract

def extract_text_from_image(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    return text
