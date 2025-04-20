from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit(request: Request):
    form_data = await request.form()
    user_text = form_data.get("user_text", "")
    return f"<div class='message'>{user_text}</div>"

@app.post("/upload-audio")
async def upload_audio(audio_file: UploadFile = File(...)):
    # Save the audio file
    file_path = os.path.join(UPLOAD_DIR, audio_file.filename)
    with open(file_path, "wb") as f:
        content = await audio_file.read()
        f.write(content)
    return {
        "message": "Audio recorded successfully!",
        "filename": audio_file.filename}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)