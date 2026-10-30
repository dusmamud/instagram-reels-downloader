import sys
from typing import Any, Dict

import yt_dlp
from rich.prompt import Confirm, Prompt

from reels_dl import config
from reels_dl.core.downloader import IgReelsDownloader, is_instagram_url
from reels_dl.ui.banner import display_preview_card, print_banner
from reels_dl.utils.system import check_dependencies, console, log_warning


def fetch_reel_preview(url: str, auth_mode: str = "none", browser: str = None, cookiefile: str = None) -> Dict[str, Any]:
    """Real yt-dlp metadata fetch, no download. Returns {} on failure."""
    ydl_opts: Dict[str, Any] = {"quiet": True, "no_warnings": True, "noplaylist": True}
    if auth_mode == "browser" and browser:
        ydl_opts["cookiesfrombrowser"] = (browser,)
    elif auth_mode == "cookiefile" and cookiefile:
        ydl_opts["cookiefile"] = str(cookiefile)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info or {}
    except Exception:
        return {}


def _interactive_loop(output_dir: str = None):
    active_output = output_dir or config.OUTPUT_DIR
    print_banner(output_dir=active_output)
    while True:
        console.print("\n" + "─" * 50, style="dim")
        url = Prompt.ask("[bold cyan]Instagram Reel URL[/bold cyan] ([bold red]q[/bold red] to quit)").strip()
        if url.lower() in ("q", "quit", "exit"):
            console.print("\n[bold green]Bye! Enjoy your reels![/bold green]\n")
            break
        if not url:
            continue
        if not is_instagram_url(url):
            log_warning("Ye Instagram Reel link nahi lag raha. Dobara sahi link daalo.")
            continue

        with console.status("[bold yellow]Reel check kar rahe hain..."):
            info = fetch_reel_preview(url)
        if info:
            display_preview_card(info)
        else:
            log_warning("Preview nahi mila, phir bhi download try kar sakte ho (shayad login chahiye).")

        console.print("\n[bold yellow]Step 1: Quality chuno[/bold yellow]")
        console.print("  [1] Best (default)   [2] 1080p   [3] 720p   [4] 480p")
        q_choice = Prompt.ask("Quality", choices=["1", "2", "3", "4"], default="1")
        quality = {"1": "best", "2": "1080", "3": "720", "4": "480"}[q_choice]

        console.print("\n[bold yellow]Step 2: Format chuno[/bold yellow]")
        fmt_choice = Prompt.ask("Format", choices=["1", "2"], default="1")
        video_format = "mp4" if fmt_choice == "1" else "webm"
        if fmt_choice == "1":
            console.print("  MP4 chuna gaya (sab players me chalega)")
        else:
            console.print("  WebM chuna gaya")

        embed_thumbnail = Confirm.ask("Thumbnail video me embed karna hai?", default=False)

        console.print("\n[bold yellow]Step 3: Login / Cookies[/bold yellow]")
        console.print("  [1] No login (default, public reels)  [2] Firefox cookies  [3] Chrome cookies  [4] cookies.txt file")
        auth_choice = Prompt.ask("Mode", choices=["1", "2", "3", "4"], default="1")
        auth_mode, browser, cookiefile = "none", None, None
        if auth_choice == "2":
            auth_mode, browser = "browser", "firefox"
        elif auth_choice == "3":
            auth_mode, browser = "browser", "chrome"
        elif auth_choice == "4":
            auth_mode = "cookiefile"
            cookiefile = Prompt.ask("cookies.txt ka full path").strip(' "\'')

        downloader = IgReelsDownloader(
            output_dir=active_output,
            quality=quality,
            video_format=video_format,
            auth_mode=auth_mode,
            browser=browser,
            cookiefile=cookiefile,
            embed_thumbnail=embed_thumbnail,
        )
        downloader.download(url)

        if not Confirm.ask("\n[bold cyan]Ek aur reel download karni hai?[/bold cyan]", default=True):
            console.print("\n[bold green]Sab ho gaya! Enjoy![/bold green]\n")
            break


def run_interactive_session(output_dir: str = None):
    if not check_dependencies():
        sys.exit(1)
    try:
        _interactive_loop(output_dir=output_dir)
    except (KeyboardInterrupt, EOFError):
        console.print("\n\n[bold yellow]Cancelled by user. Bye![/bold yellow]\n")
        sys.exit(0)
