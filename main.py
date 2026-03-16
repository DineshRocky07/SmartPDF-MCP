from fastapi import FastAPI, UploadFile, File
import fitz  # This is the PyMuPDF library
from google import genai #day2

client =genai.Client(api_key="AIzaSyDzH8rC2n-XlqB1BiA-xghQ3W2xMAYRMdw")

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

    # 4. Give the AI its instructions
    ai_prompt = f"""
    You are an expert HR assistant. Read the following resume text.
    Extract the candidate's Full Name, their Role/Title, their Phone Number, and a list of their Top 5 Technical Skills.
    Return the response cleanly and professionally.
    
    Resume Text:
    {extracted_text}
    """
    # 5. Send the text to Gemini
    response= client.models.generate_content(
        model='gemini-2.5-flash',
        contents= ai_prompt
    )

    return{
            "filename": file.filename,
            "content_type": file.content_type,
            "status": "File uploaded successfully..",
            # We slice [:500] so it only shows the first 500 characters in Swagger,
            # otherwise, a 3-page resume will flood your screen!
            #"text_preview": extracted_text[:500]

            "ai_extacted_datas": response.text
   
    }