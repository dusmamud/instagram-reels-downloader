# Troubleshooting

## 1. `externally-managed-environment` (PEP 668)
Ubuntu/Debian blocks system-wide `pip install`. Do not use
`--break-system-packages`. Use a venv or pipx instead — see INSTALLATION.md.

## 2. `ffmpeg not found`
```bash
sudo apt install -y ffmpeg
ffmpeg -version
```
ffmpeg is required to merge video + audio into one MP4. Without it,
yt-dlp cannot finish a reel download.

## 3. `login required` / private reel
Public reels usually work without login. If you get login/private errors:
```bash
python main.py "URL" --browser firefox
python main.py "URL" --cookies cookies.txt
```
Never share your `cookies.txt`. Export it only from your own browser
(e.g. with a "Get cookies.txt" extension) and keep it out of git.

## 4. 429 / rate limit
The tool retries with backoff. If it keeps failing, wait a while and try
again with fewer reels at once, or use `--dry-run` first to check access.

## 5. Wrong quality / file is smaller than expected
Instagram reels are usually 720p or 1080p at most. Asking for `best` does
not upscale a reel — it takes the best stream Instagram actually serves.
Check what exists with:
```bash
python main.py "URL" -F
```

## 6. File name looks different from the reel title
Reel titles can contain characters that are illegal on Windows
(`\ / : * ? " < > |`). The tool strips those and, in clean mode, replaces
spaces with hyphens. Use `-n formal` for a more readable name.

## 7. `yt-dlp` is old and extraction fails
Instagram changes its pages often. Update yt-dlp inside your venv:
```bash
pip install -U yt-dlp
```

## 8. Download folder confusion
By default, when you run from the project folder, files go to
`instagram-reels-downloader/downloads/`. From any other folder, they go to
`./downloads/` in that folder. Override with `-o` or the env var:
```bash
python main.py "URL" -o ~/Videos/reels
IG_REELS_DOWNLOAD_DIR=~/Videos/reels python main.py "URL"
```
