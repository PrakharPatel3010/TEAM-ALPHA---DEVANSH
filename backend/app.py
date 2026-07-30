from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

from services.chunker import chunk_text
from services.pdf_reader import extract_text_from_pdf
from services.text_cleaner import clean_text
from services.storage_service import store_chunks
from services.retrieval_service import retrieve_chunks

from summarize import summarize_text


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ------------------------
# Request Models
# ------------------------

class SearchRequest(BaseModel):
    question: str


class SummaryRequest(BaseModel):
    filename: str


# ------------------------
# Routes
# ------------------------

@app.get("/")
def home():
    return {"message": "Backend is working!"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text

    text = extract_text_from_pdf(file_path)

    text = clean_text(text)

    # Save extracted text

    txt_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename + ".txt"
    )

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Create embeddings

    chunks = chunk_text(text)

    store_chunks(chunks, file.filename)

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "chunks_created": len(chunks)
    }


@app.post("/search")
def search(request: SearchRequest):

    results = retrieve_chunks(request.question)

    return {
        "question": request.question,
        "documents": results["documents"][0]
    }


@app.post("/summarize")
async def summarize(request: SummaryRequest):

    txt_path = os.path.join(
        UPLOAD_FOLDER,
        request.filename + ".txt"
    )

    if not os.path.exists(txt_path):
        raise HTTPException(
            status_code=404,
            detail="Paper not uploaded."
        )

    with open(txt_path, "r", encoding="utf-8") as f:
        paper_text = f.read()

    summary = summarize_text(paper_text)

    return summary