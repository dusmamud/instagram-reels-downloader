import re


def sanitize_name(name: str) -> str:
    """Remove filesystem-illegal characters and collapse whitespace."""
    cleaned = re.sub(r'[\\/:*?"<>|]', "", name or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "Unknown"


def format_filename(uploader: str, title: str, reel_id: str, ext: str, naming_style: str = "clean") -> str:
    """Build a final filename. Clean = no spaces, Formal = readable with spaces."""
    uploader = sanitize_name(uploader)
    title = sanitize_name(title)
    reel_id = sanitize_name(reel_id)
    if naming_style == "formal":
        base = f"{uploader} - {title} [{reel_id}]"
    else:
        base = f"{uploader}-{title}-{reel_id}".replace(" ", "-")
        base = re.sub(r"-+", "-", base)
    # Keep filenames usable on Windows / long paths.
    if len(base) > 150:
        base = base[:150].rstrip("-")
    return f"{base}.{ext}"
