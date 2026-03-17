#from fastapi import FastAPI, UploadFile, File
import fitz  # This is the PyMuPDF library
from google import genai #day2
from google.genai import types # <--- To configure the AI's strict rules
from pydantic import BaseModel # <---  The tool that creates our "Bento Box"
import json # <-- Built-in tool to clean up the final output
from mcp.server.fastmcp import FastMCP # <--- NEW: The MCP Server library
import os      
import glob    
import time

# 1. Initialize the MCP Server (This replaces FastAPI)
mcp = FastMCP("SmartPDF-MCP")

# 2. Define the exact "Bento Box" format we want the AI to return
class ResumeData(BaseModel):
    full_name: str
    role_title: str
    phone_number: str
    top_5_technical_skills: list[str]

client =genai.Client(api_key="xxx")

@mcp.tool()
def ExtractResumeData(file_path: str ) -> str:
    """Reads a PDF resume from the local computer and extracts structured JSON data."""
    
    # 2. Open the PDF using the fitz library
    doc = fitz.open(file_path)
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

    return response.text

   #builk Upload Endpoint
@mcp.tool()
def builk_upload(folder_path: str) -> str:
    """Reads all PDF resumes from a local folder and extracts structured JSON data for each."""
    
    #1.pattern
    search_pattern =os.path.join(folder_path,"*.pdf")
    pdf_files =glob.glob(search_pattern)

    if not pdf_files:
        return '{"message": "No PDF files found in this folder."}'
    
    all_resumes_list = []

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path}...")

        doc = fitz.open(pdf_path)

        extracted_text = ""
        for page in doc:
             extracted_text += page.get_text()
        doc.close()

    ai_prompt = f"Extract Full Name, Role, Phone Number, and Top 5 Skills.\nResume Text:\n{extracted_text}"
    response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=ai_prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=ResumeData,
            ),
        )
    # Add the extracted JSON dictionary to our master list
    resume_dict = json.loads(response.text)
    all_resumes_list.append(resume_dict)

    # 3. THE SAFETY BRAKE: Pause for 4 seconds before the next one!
    time.sleep(4) 

    # 4. Return the massive list of all 10 processed resumes!
    return json.dumps(all_resumes_list, indent=2)