import logging
from pathlib import Path
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

logger = logging.getLogger(__name__)

# Video configuration
FPS = 1  # 1 slide per second; adjust as needed
DURATION_PER_SLIDE = 15  # seconds per slide


def create_video(slide_paths: list, output_path: Path):
    """
    Create a video from a list of slide image paths.
    """
    try:
        logger.info(f"Creating video at {output_path} from {len(slide_paths)} slides")

        if not slide_paths:
            raise ValueError("No slides provided for video creation")

        clip = ImageSequenceClip(slide_paths, fps=FPS)
        clip = clip.with_duration(DURATION_PER_SLIDE)  # uniform duration per slide

        clip.write_videofile(str(output_path), codec="libx264")

        logger.info(f"Video saved: {output_path}")
        return output_path

    except Exception:
        logger.exception("Video creation failed")
        raise
