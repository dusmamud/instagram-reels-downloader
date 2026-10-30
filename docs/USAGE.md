# Usage Guide

## Interactive mode
```bash
python main.py
```
URL daalo, quality chuno (best/1080/720/480), format chuno (MP4/WebM),
login mode chuno, download ho jayega. `q` likh kar bahar niklo.

## CLI examples
```bash
# Best quality MP4
python main.py "https://www.instagram.com/reel/REEL_ID/"

# 720p
python main.py "https://www.instagram.com/reel/REEL_ID/" -q 720

# WebM
python main.py "https://www.instagram.com/reel/REEL_ID/" -f webm

# Dry-run (bina save kiye check)
python main.py "https://www.instagram.com/reel/REEL_ID/" --dry-run

# Formats list
python main.py "https://www.instagram.com/reel/REEL_ID/" -F

# Thumbnail embed karo
python main.py "https://www.instagram.com/reel/REEL_ID/" --thumbnail

# Ek saath kayi URLs
python main.py "URL1" "URL2" -q 1080

# Batch file (har line ek URL, # wali line comment)
python main.py --batch-file reels.txt

# Custom output folder
python main.py "URL" -o ~/Videos/reels

# Formal filename: "Uploader - Title [ID].mp4"
python main.py "URL" -n formal
```

## Batch file example (reels.txt)
```
https://www.instagram.com/reel/AAA/
https://www.instagram.com/reel/BBB/
# ye line comment hai, ignore hogi
```

## Troubleshooting
- `login required / private`: `--browser firefox` ya `--cookies cookies.txt` try karo.
- `ffmpeg not found`: `sudo apt install ffmpeg` (Linux) karo, phir dobara chalao.
- `externally-managed-environment`: system pip me mat daalo, venv ya pipx use karo (INSTALLATION.md dekho).
- Rate limit 429: tool khud retry karta hai, thoda wait karke dobara chalao.
