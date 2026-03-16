from fastapi import FastAPI, UploadFile, File
import fitz  # This is the PyMuPDF library

app = FastAPI(
    title="Pdf Upload API",
    description="A simple API to upload files using FastAPI",
    version="1.0.0",
)
@app.get("/")
async def root():
    return {"message": "server is running in the port http://127.0.0.1:8000/docs to see the swagger documentation"}

@app.post("/upload/")
async def upload_file(file: UploadFile =File(...)):
    # 1. Read the uploaded file into your computer's memory
    file_content =await file.read()
    # 2. Open the PDF using the fitz library
    doc = fitz.open(stream=file_content,filetype='pdf')
    # 3. Loop through every page and pull out the text
    extracted_text = ""
    for page in doc:
         extracted_text += page.get_text()
    doc.close()

    return{
            "filename": file.filename,
            "content_type": file.content_type,
            "status": "File uploaded successfully..",
            # We slice [:500] so it only shows the first 500 characters in Swagger,
            # otherwise, a 3-page resume will flood your screen!
            "text_preview": extracted_text[:500]
   
    }