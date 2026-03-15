import os
import difflib
import pymupdf
from collections import deque
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

load_dotenv(override=True)
os.environ["GOOGLE_CLOUD_PROJECT"] = "trygcp-ai-488808"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lecture_notes"))


# --- TOOL 1: List the folders and files ---
def list_library() -> str:
    """Scans the lecture_notes folder and returns a structured list of subjects and files."""
    if not os.path.exists(BASE_DIR):
        return "Your library is currently empty."

    library_structure = "Here is your current library:\n"

    # We look at the first level for Subjects (Folders)
    for subject in os.listdir(BASE_DIR):
        subject_path = os.path.join(BASE_DIR, subject)
        if os.path.isdir(subject_path):
            library_structure += f"\nSubject: {subject}\n"
            # List the files inside that subject
            files = [f for f in os.listdir(subject_path) if f.endswith(('.pdf', '.pptx'))]
            if files:
                for f in files:
                    library_structure += f"  - {f}\n"
            else:
                library_structure += "  (No files in this subject yet)\n"

    return library_structure


# --- TOOL 2: Read a specific file (BFS version) ---
def read_lecture_file(filename_query: str) -> str:
    """Searches for a file using BFS and reads it."""
    queue = deque([BASE_DIR])
    all_files = []
    file_path_map = {}

    while queue:
        current_dir = queue.popleft()
        try:
            for entry in os.scandir(current_dir):
                if entry.is_dir():
                    queue.append(entry.path)
                elif entry.is_file() and entry.name.endswith(('.pdf', '.pptx')):
                    all_files.append(entry.name)
                    file_path_map[entry.name] = entry.path
        except PermissionError:
            continue

    matches = difflib.get_close_matches(filename_query, all_files, n=1, cutoff=0.3)
    if not matches:
        return f"Error: Could not find '{filename_query}'."

    target_path = file_path_map[matches[0]]
    extracted_text = ""
    with pymupdf.open(target_path) as doc:
        for page in doc:
            extracted_text += page.get_text()
    return extracted_text


# --- THE AGENT ---
root_agent = Agent(
    name="Lecture_Pro",
    model="gemini-3-flash-preview",  # Updated model name
    tools=[list_library, read_lecture_file],  # Added the new tool here
    instruction="""
    You are an academic expert. 
    1. If the user asks what files or subjects they have, use the `list_library` tool.
    2. If the user asks to summarize or quiz them on a specific file, use `read_lecture_file`.
    3. When listing subjects and chapters, present them in a clean, organized list.
    """
)