#from fastapi import FastAPI, UploadFile, File
import fitz  # This is the PyMuPDF library
from google import genai #day2
from google.genai import types # <--- To configure the AI's strict rules
from pydantic import BaseModel # <---  The tool that creates our "Bento Box"
import json # <-- Built-in tool to clean up the final output
from mcp.server.fastmcp import FastMCP # <--- NEW: The MCP Server library

# 1. Initialize the MCP Server (This replaces FastAPI)
mcp = FastMCP("SmartPDF-MCP")

# 2. Define the exact "Bento Box" format we want the AI to return
class ResumeData(BaseModel):
    full_name: str
    role_title: str
    phone_number: str
    top_5_technical_skills: list[str]

client =genai.Client(api_key="xxxxx-xxxx")

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