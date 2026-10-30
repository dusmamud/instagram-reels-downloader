import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import yt_dlp
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from reels_dl import config
from reels_dl.utils.cleanup import cleanup_partial_files
from reels_dl.utils.formatters import format_filename
from reels_dl.utils.system import console, log_error, log_info, log_success, log_warning


def is_instagram_url(url: str) -> bool:
    """True only for instagram.com links (reel / reels / p are the useful ones)."""
    url = (url or "").strip().lower()
    if "instagram.com" not in url:
        return False
    return any(part in url for part in ("/reel/", "/reels/", "/reel", "/p/")) or "instagram.com/reel" in url


def quality_format_spec(quality: str, video_format: str = "mp4") -> str:
    """Map a user quality to a real yt-dlp format selector."""
    quality = (quality or "best").lower()
    if quality == "best":
        return "bv*+ba/best"
    if quality in ("1080", "720", "480"):
        height = quality
        return f"bv[height<={height}]+ba/best"
    # Fallback: treat anything else as best, never crash on a typo.
    return "bv*+ba/best"


class IgReelsDownloader:
    def __init__(
        self,
        output_dir: Optional[str] = None,
        quality: str = config.DEFAULT_QUALITY,
        video_format: str = config.DEFAULT_FORMAT,
        auth_mode: str = config.DEFAULT_AUTH_MODE,
        browser: Optional[str] = None,
        cookiefile: Optional[str] = None,
        dry_run: bool = False,
        embed_thumbnail: bool = False,
        max_retries: int = config.MAX_RETRIES,
        retry_delay: int = config.RETRY_DELAY,
    ):
        self.output_dir = Path(output_dir or config.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.quality = (quality or "best").lower()
        self.video_format = (video_format or "mp4").lower()
        self.dry_run = dry_run
        self.embed_thumbnail = embed_thumbnail
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.cookiefile = Path(cookiefile) if cookiefile else None
        self.browser = browser
        if cookiefile:
            self.auth_mode = "cookiefile"
        elif browser:
            self.auth_mode = "browser"
        else:
            self.auth_mode = auth_mode or "none"

        self.progress: Optional[Progress] = None
        self.task_id = None

    def _progress_hook(self, d: Dict[str, Any]):
        if self.dry_run:
            return
        status = d.get("status")
        if status == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes") or 0
            if self.progress is None:
                self.progress = Progress(
                    SpinnerColumn(),
                    TextColumn("[bold cyan]{task.description}"),
                    BarColumn(bar_width=40),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=console,
                )
                self.progress.start()
                self.task_id = self.progress.add_task("Downloading reel...", total=total_bytes)
            if self.task_id is not None:
                if total_bytes and self.progress.tasks[self.task_id].total != total_bytes:
                    self.progress.update(self.task_id, total=total_bytes)
                self.progress.update(self.task_id, completed=downloaded)
        elif status == "finished":
            if self.progress and self.task_id is not None:
                self.progress.update(self.task_id, description="[bold green]Download complete! Merging...")
                self.progress.stop()
                self.progress = None
                self.task_id = None

    def _build_ydl_opts(self, simulate_override: Optional[bool] = None) -> Dict[str, Any]:
        is_simulated = self.dry_run if simulate_override is None else simulate_override
        out_template = str(
            self.output_dir / "%(uploader,channel)s - %(title)s [%(id)s].%(ext)s"
        )
        postprocessors = []
        if not is_simulated:
            postprocessors.append({"key": "FFmpegMetadata", "add_metadata": True})
            if self.embed_thumbnail:
                postprocessors.append({"key": "EmbedThumbnail"})
        ydl_opts: Dict[str, Any] = {
            "format": quality_format_spec(self.quality, self.video_format),
            "merge_output_format": self.video_format,
            "outtmpl": out_template,
            "writethumbnail": bool(self.embed_thumbnail and not is_simulated),
            "postprocessors": postprocessors,
            "noplaylist": True,
            "nopart": True,
            "continuedl": False,
            "windowsfilenames": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self._progress_hook],
            "retries": 3,
            "fragment_retries": 3,
            "socket_timeout": config.SOCKET_TIMEOUT,
            "simulate": is_simulated,
        }
        if self.auth_mode == "browser":
            ydl_opts["cookiesfrombrowser"] = (self.browser or config.DEFAULT_BROWSER,)
        elif self.auth_mode == "cookiefile" and self.cookiefile:
            ydl_opts["cookiefile"] = str(self.cookiefile)
        return ydl_opts

    def list_formats(self, url: str) -> bool:
        from reels_dl.ui.banner import display_formats_table

        if not is_instagram_url(url):
            log_error("Ye Instagram URL nahi lag raha. Reel ka link daalo, jaise instagram.com/reel/...")
            return False
        log_info(f"Formats nikal rahe hain: [white]{url}[/white]")
        ydl_opts = self._build_ydl_opts(simulate_override=True)
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    log_error("Is URL se koi info nahi mili.")
                    return False
                display_formats_table(info.get("formats", []), title=f"Formats: {info.get('title', 'Unknown')}")
                return True
        except Exception as e:
            log_error(f"Formats nikalne me fail: {e}")
            return False

    def download(self, url: str, naming_style: str = "clean") -> bool:
        url = (url or "").strip()
        if not is_instagram_url(url):
            log_error("Ye Instagram Reel URL nahi hai. Sahi link daalo: instagram.com/reel/... ya /reels/...")
            return False

        if self.dry_run:
            log_info(f"[DRY-RUN] Sirf check kar rahe hain, download nahi hoga: [white]{url}[/white]")
        else:
            log_info(f"Download shuru: [white]{url}[/white]")
            log_info(f"Quality: [green]{self.quality}[/green] | Format: [green]{self.video_format.upper()}[/green] | Folder: [dim]{self.output_dir}[/dim]")
            if self.auth_mode != "none":
                log_info(f"Auth mode: [cyan]{self.auth_mode}[/cyan]")

        cleanup_partial_files(self.output_dir)
        attempt = 0
        current_delay = self.retry_delay
        while attempt < self.max_retries:
            attempt += 1
            try:
                ydl_opts = self._build_ydl_opts()
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=not self.dry_run)
                    if not info:
                        log_error("Koi track info nahi mili.")
                        return False
                    title = info.get("title", "Unknown Reel")
                    uploader = info.get("uploader") or info.get("channel") or "Unknown"
                    reel_id = info.get("id", "unknown")

                    if self.dry_run:
                        log_success(f"[DRY-RUN] Mil gaya: [bold white]{uploader} - {title}[/bold white]")
                        return True

                    raw_filename = ydl.prepare_filename(info)
                    target = Path(raw_filename)
                    if not target.exists():
                        # yt-dlp merged file ka naam kabhi alag ho sakta hai, newest file lo.
                        candidates = sorted(
                            self.output_dir.glob(f"*{reel_id}*.{self.video_format}"),
                            key=lambda p: p.stat().st_mtime,
                            reverse=True,
                        )
                        if candidates:
                            target = candidates[0]

                    if target.exists():
                        final_name = format_filename(uploader, title, reel_id, self.video_format, naming_style)
                        final_path = self.output_dir / final_name
                        if target != final_path:
                            try:
                                if final_path.exists():
                                    final_path.unlink(missing_ok=True)
                                target.replace(final_path)
                                target = final_path
                            except Exception:
                                pass
                        size_mb = target.stat().st_size / (1024 * 1024)
                        log_success(f"Ho gaya: [bold white]{target.name}[/bold white] ([green]{size_mb:.2f} MB[/green])")
                    else:
                        log_success(f"Ho gaya: [bold white]{uploader} - {title}[/bold white]")
                    return True
            except Exception as e:
                if self.progress:
                    try:
                        self.progress.stop()
                    except Exception:
                        pass
                    self.progress = None
                msg = str(e).lower()
                retryable = True
                if "login required" in msg or "private" in msg or "log in" in msg:
                    log_warning("Ye reel login/private lag rahi hai. --browser firefox ya --cookies cookies.txt try karo.")
                    retryable = False
                if "429" in msg or "too many requests" in msg:
                    current_delay = max(current_delay, 10.0) * 1.5
                if not retryable or attempt >= self.max_retries:
                    log_error(f"{attempt} attempt ke baad fail: {e}")
                    return False
                log_warning(f"Attempt {attempt} fail. {current_delay:.1f}s me dobara try...")
                time.sleep(current_delay)
                current_delay *= config.BACKOFF_FACTOR
        return False

    def download_many(self, urls: List[str], naming_style: str = "clean") -> List[Dict[str, Any]]:
        results = []
        for url in urls:
            url = url.strip()
            if not url or url.startswith("#"):
                continue
            ok = self.download(url, naming_style=naming_style)
            results.append({"url": url, "success": ok})
        return results
