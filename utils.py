import fitz
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

HF_API_KEY=os.getenv("HF_API_KEY")

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3", token=os.getenv("HF_API_KEY"),)


def extract_text_from_pdf(file_path:str)->str:
    text=""
    with fitz.open(file_path) as pdf:

        for page in pdf:
            text+=page.get_text()
        return text

def generate_questions(resume_text,job_role):
    prompt= f"""
    You are an interviewer for a {job_role}.
    Based on this resume:{resume_text},
    generate 5 technical and 3 behavioral interview
    questions.Return them as a numbered list.
    """

    response=client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "system", "content": "You are a professional AI interviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response

def evaluate_answer(answer, question, job_role):
    prompt=f"""
    Evaluate this candidate's answer for this role{job_role}.
    Question:{question}
    Answer{answer}

    Provide:
    - Score(0-10)
    - Strengths
    - Weaknesses
    - Suggestions
    
    """

    response=client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "system", "content": "Evaluate this candidate's answer for this role.If the answer provided is not relevant to the question posted,then be harsh on evaluating and the answer and point at out what's relaly missing in the answer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response
