import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

from presentation_agent.tools.slide_renderer import render_slide

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Presentation Agent API is running"}


@app.post("/render-slide")
def render_slide_api():
    # Example slide
    slide = {"title": "Step 1 Slide", "content": ["Line 1", "Line 2", "Line 3", "Line 4"]}
    output_path = Path("slide_test.png")
    render_slide(slide, output_path)
    return {"slide_path": str(output_path)}


@app.get("/download-slide")
def download_slide():
    file_path = Path("slide_test.png")
    if file_path.exists():
        logger.info(f"Downloading slide: {file_path}")
        return FileResponse(file_path, media_type="image/png", filename="slide_test.png")
    else:
        logger.warning("slide_test.png not found")
        return {"error": "Slide not found. Generate it first with /render-slide"}
