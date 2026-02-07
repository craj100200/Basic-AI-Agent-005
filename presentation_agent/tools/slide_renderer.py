import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# Slide image configuration
WIDTH = 1280
HEIGHT = 720
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (255, 200, 0)
FONT_SIZE_TITLE = 60
FONT_SIZE_CONTENT = 40
MARGIN = 100


def render_slide(slide: dict, output_path: Path):
    """
    Render a single slide (dict with title + content list) to an image file.
    """
    try:
        logger.info(f"Rendering slide to {output_path}")
        img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", FONT_SIZE_TITLE)
            font_content = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE_CONTENT)
        except:
            font_title = ImageFont.load_default()
            font_content = ImageFont.load_default()

        # Draw title
        draw.text((MARGIN, MARGIN), slide["title"], fill=TITLE_COLOR, font=font_title)

        # Draw content
        y_offset = MARGIN + FONT_SIZE_TITLE + 40
        for line in slide["content"]:
            draw.text((MARGIN, y_offset), line, fill=TEXT_COLOR, font=font_content)
            y_offset += FONT_SIZE_CONTENT + 10

        # Save image
        img.save(output_path)
        logger.info(f"Slide saved: {output_path}")
        return output_path

    except Exception:
        logger.exception("Slide render failed")
        raise


def render_all_slides(slides: list, output_dir: Path):
    """
    Render all slides to PNG images in output_dir.
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for i, slide in enumerate(slides, start=1):
            filename = f"slide_{i:03d}.png"
            path = output_dir / filename
            render_slide(slide, path)
            paths.append(str(path))
        logger.info(f"{len(paths)} slides rendered in {output_dir}")
        return paths
    except Exception:
        logger.exception("Render all slides failed")
        raise

