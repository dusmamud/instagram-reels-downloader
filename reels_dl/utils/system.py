import shutil

from rich.console import Console
from rich.panel import Panel

console = Console()


def log_info(msg: str):
    console.print(f"[bold cyan][INFO][/bold cyan] {msg}")


def log_success(msg: str):
    console.print(f"[bold green][SUCCESS][/bold green] {msg}")


def log_warning(msg: str):
    console.print(f"[bold yellow][WARNING][/bold yellow] {msg}")


def log_error(msg: str):
    console.print(f"[bold red][ERROR][/bold red] {msg}")


def check_dependencies() -> bool:
    """Check the two real runtime requirements: yt-dlp (Python) and ffmpeg (binary)."""
    all_ok = True
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        all_ok = False
        console.print(
            Panel.fit(
                "[bold red]yt-dlp Python package is not installed![/bold red]\n\n"
                "Install it using:\n[bold green]pip install -U yt-dlp[/bold green]",
                title="Missing Dependency: yt-dlp",
                border_style="red",
            )
        )
    if not shutil.which("ffmpeg"):
        all_ok = False
        console.print(
            Panel.fit(
                "[bold red]ffmpeg executable was not found on your system PATH![/bold red]\n\n"
                "ffmpeg is required to merge video + audio into one MP4 file.\n"
                "Ubuntu/Debian: [bold green]sudo apt install ffmpeg[/bold green]",
                title="Missing Dependency: ffmpeg",
                border_style="red",
            )
        )
    return all_ok
