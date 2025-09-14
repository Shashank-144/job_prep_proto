from fastapi import FastAPI, UploadFile, Form
from utils import extract_text_from_pdf, generate_questions, evaluate_answer
import shutil
import os
from datetime import datetime
from db.mongodb import Feedback,feedback_collection

from fastapi.responses import RedirectResponse
app = FastAPI(title="Job Search Buddy 🚀")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running 🚀"}

# Upload Resume + Provide Job Role -> Generate Questions
@app.post('/upload-resume-and-get-questions/')
async def upload_resume(
    file: UploadFile,
    job_role: str = Form(...)
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)
    questions = generate_questions(resume_text, job_role)

    return {"questions": questions}

# Evaluate Candidate Answer
@app.post("/evaluate-answer/")
async def evaluate_candidate_answer(
    candidate_answer: str = Form(...),
    question: str = Form(...),
    job_role: str = Form(...)
):
    feedback = evaluate_answer(candidate_answer, question, job_role)
    return {"feedback": feedback}


@app.post("/feedback")
async def submit_feedback(feedback: Feedback):
    doc = feedback.dict()
    doc["created_at"] = datetime.utcnow()
    result = await feedback_collection.insert_one(doc)
    return {"message": "Feedback saved", "id": str(result.inserted_id)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
