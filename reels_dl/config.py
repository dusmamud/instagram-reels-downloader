import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent


def get_default_download_dir() -> Path:
    """Return a sensible download folder, without touching the user's home blindly."""
    env_dir = os.getenv("IG_REELS_DOWNLOAD_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()

    cwd = Path.cwd().resolve()
    if (PROJECT_ROOT / "pyproject.toml").exists() and cwd == PROJECT_ROOT.resolve():
        return PROJECT_ROOT / "downloads"
    if cwd.name.lower() in ("download", "downloads", "reels"):
        return cwd
    return cwd / "downloads"


DEFAULT_DOWNLOAD_DIR = get_default_download_dir()
OUTPUT_DIR = str(DEFAULT_DOWNLOAD_DIR)


def set_output_dir(custom_path: str):
    global OUTPUT_DIR
    if custom_path:
        OUTPUT_DIR = str(Path(custom_path).expanduser())


DEFAULT_FORMAT = "mp4"
SUPPORTED_FORMATS = ["mp4", "webm"]
DEFAULT_QUALITY = "best"
SUPPORTED_QUALITIES = ["best", "1080", "720", "480"]
DEFAULT_AUTH_MODE = "none"
DEFAULT_BROWSER = "firefox"
SUPPORTED_BROWSERS = ["firefox", "chrome", "edge", "brave"]

MAX_RETRIES = 3
RETRY_DELAY = 5
BACKOFF_FACTOR = 2.0
SOCKET_TIMEOUT = 30
