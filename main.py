import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse


from presentation_agent.tools.slide_renderer import render_slide, render_all_slides
from presentation_agent.tools.slide_parser import parse_slides
from presentation_agent.tools.video_renderer import create_video


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Folder where input files are stored
INPUT_DIR = Path("presentation_agent/workspace/input")
INPUT_DIR.mkdir(parents=True, exist_ok=True)
# Output folder
OUTPUT_DIR = Path("presentation_agent/workspace/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR = Path("presentation_agent/workspace/video")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

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


@app.get("/render_all_slides")
def api_render_slides(filename: str):
    """
    Parse the slides from a text file and render them to images.
    Returns the list of generated slide image filenames.
    Example: /render_slides?filename=slides.txt
    """
    try:
        file_path = INPUT_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"{filename} not found in {INPUT_DIR}")

        slides = parse_slides(file_path)
        paths = render_all_slides(slides, OUTPUT_DIR)

        # Return only filenames
        return {"slides": [Path(p).name for p in paths]}

    except Exception as e:
        logger.exception("Slide rendering failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate_video")
def api_generate_video(slide_filename: str, video_name: str = "presentation.mp4"):
    """
    Generate an MP4 video from slides in slides.txt
    Example: /generate_video?slide_filename=slides.txt&video_name=demo.mp4
    """
    try:
        input_file = INPUT_DIR / slide_filename
        if not input_file.exists():
            raise HTTPException(status_code=404, detail=f"{slide_filename} not found")

        slides = parse_slides(input_file)
        slide_images = render_all_slides(slides, OUTPUT_DIR)

        video_path = VIDEO_DIR / video_name
        create_video(slide_images, video_path)

        return {"video_file": video_name}

    except Exception as e:
        logger.exception("Video generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download_video/{video_name}")
def download_video(video_name: str):
    """
    Download the generated video by name
    """
    video_path = VIDEO_DIR / video_name
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"{video_name} not found")
    return FileResponse(video_path)
