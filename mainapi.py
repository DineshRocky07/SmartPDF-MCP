from fastapi import FastAPI, UploadFile, File
import fitz  # This is the PyMuPDF library
from google import genai #day2
from google.genai import types # <--- NEW: To configure the AI's strict rules
from pydantic import BaseModel # <--- NEW: The tool that creates our "Bento Box"
import json # <--- NEW: Built-in tool to clean up the final output
from mcp.server.fastmcp import FastMCP # <--- NEW: The MCP Server library

# 1. Initialize the MCP Server (This replaces FastAPI)
mcp = FastMCP("SmartPDF-MCP")

# 1. Define the exact "Bento Box" format we want the AI to return
class ResumeData(BaseModel):
    full_name: str
    role_title: str
    phone_number: str
    top_5_technical_skills: list[str]

client =genai.Client(api_key="xxxx")

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
        contents= ai_prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',# <--- Tell it we strictly want JSON
            response_schema=ResumeData,
        ),
    )

    return{
            "filename": file.filename,
            "content_type": file.content_type,
            "status": "File uploaded successfully..",
            # We slice [:500] so it only shows the first 500 characters in Swagger,
            # otherwise, a 3-page resume will flood your screen!
            #"text_preview": extracted_text[:500]

            "ai_extacted_datas": json.loads(response.text) # <--- Convert the AI's JSON string back into a Python dictionary   
    }