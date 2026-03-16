# SmartPDF-MCP
📑 SmartPDF-MCP: Professional Document Extraction
A high-performance FastAPI tool that uses PyMuPDF to transform messy PDF documents into clean, usable data.
🚀 What This Project Does (The Journey)
Part 1: The API Gateway (The Menu)
We built a professional API foundation using FastAPI.
The Result: An interactive dashboard (Swagger UI) that allows anyone to upload files securely.
Real-World Value: Created a bridge that lets the internet "talk" to our Python code.
Part 2: The Extraction Engine (The Kitchen)
We integrated PyMuPDF (fitz) to "rip open" PDFs and pull out the data.
The Result: Successfully processed real-world resumes, instantly extracting names, skills (Java, MySQL, Spring Boot), and contact info.
Real-World Value: This replaces hours of manual data entry with a 1-second automated pipeline.
📖 Simple Coding Dictionary
If you are looking at the code, here is what those "weird words" actually mean:
async def (The Multitasker):
Imagine a chef. A normal function stares at boiling water and does nothing else. async def allows the chef to chop onions while the water heats up. It makes the server lightning fast.
await (The Bookmark):
This tells the code: "Pause here until the file is fully downloaded, then resume exactly where you left off." It prevents the app from crashing while waiting for big files.
UploadFile (The Security Guard):
This ensures the user actually attaches a file before they are allowed to click "Submit."
fitz (The Translator):
The internal name for PyMuPDF. It’s the "brain" that knows how to read PDF formatting and turn it into simple text.
🛠️ Tech Stack
FastAPI: The high-speed web framework.
PyMuPDF (fitz): The industry-standard engine for PDF manipulation.
Uvicorn: The "engine" that keeps our server running.

Part 3: The AI Brain (The Head Chef)
We connected our data extraction pipeline to Google's Gemini 2.5 Flash AI model using the new google-genai SDK.

The Result: Instead of just spitting out a messy wall of raw text, the API now sends the text to Gemini. The AI reads it, understands the context, and intelligently extracts the candidate's exact Name, Role, Phone Number, and Technical Skills directly into the Swagger UI.

Real-World Value: This bridges the gap between traditional backend code and modern AI. We aren't just reading data anymore; we are understanding it.

Add these to your "📖 Simple Coding Dictionary":
genai.Client (The Waiter):
This is our secure connection to Google. It uses our API key to prove we are allowed in the restaurant, and it carries our raw data (the ingredients) to the AI model (the chef).

client.models.generate_content (The Order):
This is the action command. It tells the specific "Flash" chef (which is lightning-fast at reading documents) to look at our prompt and cook up an intelligent summary.

Add this to your "🛠️ Tech Stack":
Google GenAI SDK: The official Python library connecting our server to the Gemini 2.5 Flash model.