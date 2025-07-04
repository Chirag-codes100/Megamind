import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script/style elements
    for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        element.decompose()

    # Extract main text
    texts = soup.stripped_strings
    page_text = "\n".join(texts)
    return page_text
