from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import fitz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_path):
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text

@app.get("/")
def home():
    
    return {"message": "Backend is working!"}
    # Upload endpoint
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "text": text
    }