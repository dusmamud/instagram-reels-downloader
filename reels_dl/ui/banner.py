from rich.panel import Panel
from rich.table import Table

from reels_dl.utils.system import console
from reels_dl.utils.updater import check_for_updates, display_update_notification
from reels_dl.version import __version__


def print_banner(output_dir: str = ""):
    console.print(
        Panel.fit(
            f"[bold magenta]Instagram Reels Downloader[/bold magenta]  [dim]v{__version__}[/dim]\n"
            f"[dim]Output folder: {output_dir}[/dim]",
            border_style="magenta",
            title="IG Reels DL",
        )
    )
    try:
        new_version = check_for_updates()
        if new_version:
            display_update_notification(new_version)
    except Exception:
        pass


def display_preview_card(info: dict):
    table = Table(title="Reel Preview", border_style="cyan")
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_row("Title", str(info.get("title", "Unknown"))[:120])
    table.add_row("Uploader", str(info.get("uploader") or info.get("channel") or "Unknown"))
    table.add_row("ID", str(info.get("id", "Unknown")))
    duration = info.get("duration")
    if duration:
        table.add_row("Duration", f"{duration} sec")
    console.print(table)


def display_formats_table(formats: list, title: str = "Formats"):
    table = Table(title=title, border_style="green")
    table.add_column("Format ID", style="cyan")
    table.add_column("Ext", style="white")
    table.add_column("Resolution", style="white")
    table.add_column("Note", style="dim")
    for f in formats or []:
        res = f.get("resolution") or f"{f.get('width', '')}x{f.get('height', '')}".strip("x")
        table.add_row(str(f.get("format_id", "")), str(f.get("ext", "")), str(res), str(f.get("format_note", ""))[:40])
    console.print(table)
