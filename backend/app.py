from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.chunker import chunk_text
import os
import shutil
from pydantic import BaseModel

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

from services.pdf_reader import extract_text_from_pdf

@app.get("/")
def home():
    
    return {"message": "Backend is working!"}

from services.text_cleaner import clean_text
from services.storage_service import store_chunks

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    
    text = clean_text(text)

    chunks = chunk_text(text)

    store_chunks(chunks, file.filename)
    
    return {
    "message": "Upload successful",
    "filename": file.filename,
    "chunks_created": len(chunks)
}

class SearchRequest(BaseModel):
    question: str