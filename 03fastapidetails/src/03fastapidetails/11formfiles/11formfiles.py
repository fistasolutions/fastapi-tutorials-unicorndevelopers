from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional
import shutil
import os

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/files/upload/")
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the file
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    return {
        "filename": file.filename,
        "description": description,
        "content_type": file.content_type
    }

@app.post("/files/multiple/")
async def create_files(
    files: list[UploadFile] = File(...),
    description: Optional[str] = Form(None)
):
    return {
        "filenames": [file.filename for file in files],
        "description": description
    } 