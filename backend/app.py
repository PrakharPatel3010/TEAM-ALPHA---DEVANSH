from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():
    
    return {"message": "Backend is working!"}
    # Upload endpoint
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    return {
        "filename": file.filename
    }