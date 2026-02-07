import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_slides(input_file: Path):
    """
    Parse a text file into a list of slides.
    Each slide is a dict: {"title": str, "content": List[str]}
    """
    slides = []

    try:
        logger.info(f"Parsing slides from {input_file}")

        text = input_file.read_text(encoding="utf-8")

        slide_blocks = text.split("[SLIDE_START]")
        for block in slide_blocks:
            if "[SLIDE_END]" not in block:
                continue

            slide_content = block.split("[SLIDE_END]")[0].strip()

            # Extract title
            if "[TITLE_START]" in slide_content and "[TITLE_END]" in slide_content:
                title = slide_content.split("[TITLE_START]")[1].split("[TITLE_END]")[0].strip()
                content_lines = slide_content.split("[TITLE_END]")[1].strip().split("\n")
            else:
                title = "Untitled Slide"
                content_lines = slide_content.split("\n")

            content_lines = [line.strip() for line in content_lines if line.strip()]

            slides.append({"title": title, "content": content_lines})

        logger.info(f"Parsed {len(slides)} slides")
        return slides

    except Exception:
        logger.exception("Failed to parse slides")
        raise
