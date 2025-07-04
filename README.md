# Megamind

Megamind is a Python project that uses Google Gemini AI to answer questions from document content, with clear citations.  
The codebase is modular, keeping API keys secure and easy to use.

---

## 🚀 Features

- Ask questions using Google Gemini API and get quoted answers with page references.
- Modular code—easy to add new document sources or processing steps.
- Keeps your API key private (never upload your secrets).
- Ready for Streamlit or CLI use.

---

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Chirag-codes100/Megamind.git
   cd Megamind
2. Create a virtual environment (recommended):

bash
Copy
Edit
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

3. Install required dependencies:

bash
Copy
Edit
pip install -r requirements.txt

🔑 API Key Setup
Create your own config.py in the project root (not tracked by git).

Copy this template into config.py and add your actual Gemini API key:

python
Copy
Edit
# config.py
API_KEY = "your_gemini_api_key_here"
(You can also copy from config.sample.py if provided.)

Never upload your real config.py to GitHub!
It is already listed in .gitignore for your safety.

📝 Usage Example
python
Copy
Edit
from ask_gemini import ask_gemini   # Use your actual file/module name

chunks = [{'page': 1, 'text': 'Gemini is an AI developed by Google.'}]
question = "What is Gemini?"
print(ask_gemini(question, chunks))
📂 Project Structure
arduino
Copy
Edit
Megamind/
├── main.py
├── ask_gemini.py
├── config.sample.py    # Template for config.py (no real keys)
├── requirements.txt
├── README.md
└── ... (other code files/folders)

🤝 Contributing
Pull requests and suggestions are welcome!
For major changes, open an issue first to discuss what you’d like to change.

Created by Chirag Pandit
