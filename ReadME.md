# Lecture-Pro AI Agent 🎓
A smart study assistant built for the Gemini Nexus Hackathon.

## Features
- **BFS Deep Search:** Finds lecture notes even in nested folders.
- **Fuzzy Matching:** Understands what file you want even if you misspell it.
- **Automated Quizzing:** Generates summaries and MCQs from PDFs/PPTXs using Gemini 3 Flash.
- **PyMuPDF Backend:** Handles heavy image-based PDFs without memory crashes.

## Setup
1. Clone the repo.
2. Create a `.env` file with `GEMINI_API_KEY=your_key`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the agent: `adk web`.
5. Run the upload server: `python upload_server.py`.