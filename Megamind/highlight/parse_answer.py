import re

import re

def extract_text_and_page(answer):
    # Pattern 1: (Page 23): "Text..."
    match = re.search(r'\(?(Page|Slide) (\d+)\)?:?\s*["\']?(.*?)[\'"]?$', answer)
    if match:
        page = int(match.group(2))
        text = match.group(3).strip()
        return text, page
    # Pattern 2: "Text..." (Page 23)
    match = re.search(r'["\']?(.+?)["\']? \(?(Page|Slide) (\d+)\)?', answer)
    if match:
        text = match.group(1).strip()
        page = int(match.group(3))
        return text, page
    return None, None

