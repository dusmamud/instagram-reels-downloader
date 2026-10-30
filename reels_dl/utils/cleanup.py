from pathlib import Path
from typing import Union


def cleanup_partial_files(directory: Union[str, Path]) -> int:
    """Delete leftover partial download files in one folder. Returns how many were removed."""
    folder = Path(directory)
    removed = 0
    if not folder.exists():
        return 0
    for pattern in ("*.part", "*.ytdl", "*.tmp"):
        for path in folder.glob(pattern):
            try:
                if path.is_file():
                    path.unlink(missing_ok=True)
                    removed += 1
            except Exception:
                pass
    return removed
