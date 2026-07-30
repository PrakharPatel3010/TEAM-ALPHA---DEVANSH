from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

from services.chunker import chunk_text
from services.pdf_reader import extract_text_from_pdf
from services.text_cleaner import clean_text
from services.storage_service import store_chunks
from services.retrieval_service import retrieve_chunks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Models
# -----------------------------
class SearchRequest(BaseModel):
    question: str


# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Backend is working!"}


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
