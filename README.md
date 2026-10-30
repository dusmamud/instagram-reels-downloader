# Instagram Reels Downloader

[![CI Suite](https://github.com/dusmamud/instagram-reels-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/dusmamud/instagram-reels-downloader/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB)
![License](https://img.shields.io/badge/License-MIT-success.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6)

YouTube Music downloader jaisa hi CLI tool, par Instagram Reels ke liye.
Real yt-dlp engine, koi mock / placeholder download nahi hai.

## Features
- Single reel ya ek saath kayi reels (batch file se)
- Quality: best, 1080p, 720p, 480p — ye best stream Instagram serve karta hai, upscale nahi karta
- Format: MP4 (default, sab players me chalega) ya WebM
- Interactive mode: bina koi flag yaad rakhe, step-by-step
- Login-required / private reels ke liye browser cookies ya cookies.txt support
- `--dry-run`: download kiye bina sirf check karo ki reel mil rahi hai ya nahi
- `--list-formats`: available video formats dikhao
- `--thumbnail`: reel thumbnail ko video me embed karo, plus FFmpeg metadata
- PyPI update check: interactive mode me naya version ho to notification
- Progress bar, retry (429 / network glitch par), partial-file cleanup
- Clean / formal filename style

## Quick Start (Linux)

```bash
# System packages
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg

# Is project folder me
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Interactive mode (sabse easy)
python main.py

# Direct download
python main.py "https://www.instagram.com/reel/REEL_ID/" -q 720 -f mp4

# Sirf check karo, download mat karo
python main.py "https://www.instagram.com/reel/REEL_ID/" --dry-run

# Kayi reels ek saath (har line par ek URL)
python main.py --batch-file reels.txt -q best
```

Global command chahiye to:
```bash
pip install -e .
dus-ig-reels-dl "https://www.instagram.com/reel/REEL_ID/" -q 1080
```

> Note: Ubuntu/Debian par seedha system `pip install` PEP 668 se block hota hai.
> Venv ya pipx use karo, `--break-system-packages` mat lagao. Detail: `docs/INSTALLATION.md`.

## CLI Cheat Sheet

| Kaam | Command |
| ---- | ------- |
| Interactive | `python main.py` |
| Best quality | `python main.py "URL"` |
| 720p MP4 | `python main.py "URL" -q 720 -f mp4` |
| Dry-run | `python main.py "URL" --dry-run` |
| Formats list | `python main.py "URL" -F` |
| Batch file | `python main.py --batch-file reels.txt` |
| Thumbnail embed | `python main.py "URL" --thumbnail` |
| Custom folder | `python main.py "URL" -o ~/Videos/reels` |
| Formal naam | `python main.py "URL" -n formal` |

## Login wali reels

Public reels aksar bina login ke mil jati hain. Agar "login required" error aaye to:

```bash
# Firefox ke cookies se
python main.py "URL" --browser firefox

# Ya cookies.txt file se (browser extension se export ki hui)
python main.py "URL" --cookies cookies.txt
```

Apni `cookies.txt` kabhi share ya git me commit mat karo.

## Architecture

```
instagram-reels-downloader/
├── main.py                  # Launcher
├── reels_dl/
│   ├── cli.py               # CLI parser + main()
│   ├── config.py            # Output folder, defaults
│   ├── core/downloader.py   # Asli yt-dlp download logic
│   ├── ui/interactive.py    # Interactive REPL + preview
│   ├── ui/banner.py         # Banner, preview card, formats table, update notice
│   └── utils/
│       ├── system.py        # ffmpeg / yt-dlp dependency check
│       ├── formatters.py    # Filename sanitise + clean/formal style
│       ├── updater.py       # PyPI update check (fail-safe)
│       └── cleanup.py       # Partial .part/.ytdl/.tmp cleanup
├── tests/                   # Unit tests (bina network ke)
├── docs/
│   ├── USAGE.md
│   ├── INSTALLATION.md
│   └── TROUBLESHOOTING.md
├── .github/workflows/       # CI + PyPI publish
├── CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
├── TEST_GUIDE.md, DISCLAIMER.md, LICENSE
└── downloads/               # Default output folder
```

## Testing

```bash
pip install -r requirements-dev.txt
python -m unittest discover tests
# ya
pytest
ruff check reels_dl tests
```

Detail ke liye `TEST_GUIDE.md` dekho. Unit tests me koi real reel download nahi hota.

## Documentation Hub

| Doc | Kya milega |
| --- | ---------- |
| [USAGE.md](docs/USAGE.md) | Saare commands aur batch file example |
| [INSTALLATION.md](docs/INSTALLATION.md) | Linux install, venv, PEP 668 |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Login, 429, ffmpeg, quality issues |
| [TEST_GUIDE.md](TEST_GUIDE.md) | Test architecture aur rules |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution rules |

## Legal Note

Sirf apne khud ke content, ya jiska permission / Creative Commons license ho, usko download karo.
Kisi aur ka copyrighted content bina permission ke download karna galat hai.
Poora disclaimer `DISCLAIMER.md` me hai. Ye tool koi DRM bypass nahi karta.
