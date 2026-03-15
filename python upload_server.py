import os
from fastapi import FastAPI, UploadFile, Form
import uvicorn

app = FastAPI()
BASE_DIR = "./lecture_notes"


@app.post("/upload")
async def upload_file(subject: str = Form(...), file: UploadFile = Form(...)):
    """Receives a file from the Android app and saves it to the right folder."""
    subject_path = os.path.join(BASE_DIR, subject)
    os.makedirs(subject_path, exist_ok=True)

    file_path = os.path.join(subject_path, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"message": f"Successfully uploaded {file.filename} to {subject}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Runs on port 8001 so it doesn't clash with ADK