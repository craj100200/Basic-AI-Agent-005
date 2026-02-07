import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse


from presentation_agent.tools.slide_renderer import render_slide
from presentation_agent.tools.slide_parser import parse_slides


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Folder where input files are stored
INPUT_DIR = Path("presentation_agent/workspace/input")
INPUT_DIR.mkdir(parents=True, exist_ok=True)


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


@app.get("/parse_slides")
def api_parse_slides(filename: str):
    """
    API to parse slides from a text file.
    Example: /parse_slides?filename=slides.txt
    """
    try:
        file_path = INPUT_DIR / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"{filename} not found in {INPUT_DIR}")

        slides = parse_slides(file_path)
        return JSONResponse(content={"slides": slides})

    except Exception as e:
        logger.exception("Slide parsing failed")
        raise HTTPException(status_code=500, detail=str(e))
