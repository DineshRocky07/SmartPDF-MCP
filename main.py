from fastapi import FastAPI, UploadFile, File

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
    return{
            "filename": file.filename,
            "content_type": file.content_type,
            "status": "File uploaded successfully.."
        
   
    }