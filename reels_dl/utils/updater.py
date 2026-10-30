import json
import urllib.request
from typing import Optional, Tuple

from rich.panel import Panel

from reels_dl.utils.system import console
from reels_dl.version import __version__


def parse_version(ver_str: str) -> Tuple[int, ...]:
    clean_ver = ver_str.strip().lstrip("v")
    parts = []
    for part in clean_ver.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            break
    return tuple(parts)


def check_for_updates(package_name: str = "dus-ig-reels-dl", timeout: float = 1.5) -> Optional[str]:
    """Query PyPI for a newer version. Returns the version string, else None. Never raises."""
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        req = urllib.request.Request(url, headers={"User-Agent": f"dus-ig-reels-dl/{__version__}"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                latest_ver = data.get("info", {}).get("version")
                if latest_ver and parse_version(latest_ver) > parse_version(__version__):
                    return latest_ver
    except Exception:
        return None
    return None


def display_update_notification(latest_version: str):
    if not latest_version:
        return
    console.print(
        Panel(
            f"[bold yellow]Update Available![/bold yellow] "
            f"[dim white]{__version__}[/dim white] -> [bold green]{latest_version}[/bold green]\n"
            f"[dim]Run to upgrade:[/dim] [bold cyan]pip install --upgrade dus-ig-reels-dl[/bold cyan]",
            border_style="yellow",
            padding=(0, 2),
        )
    )
