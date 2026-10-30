# Installation (Linux)

## System requirements
- Python 3.10 ya upar
- ffmpeg (video + audio merge ke liye zaroori)
- Internet

## Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg
```

## Project setup (venv, recommended)
```bash
cd instagram-reels-downloader
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --help
```

## PEP 668 error se bachna
Ubuntu/Debian par seedha `pip install` system Python me block hota hai
(`externally-managed-environment`). Isliye:
- venv use karo (upar wala tarika), ya
- global install ke liye pipx: `pipx install .` (pipx ke baad terminal dobara kholo)

`--break-system-packages` use mat karo, system Python kharab ho sakta hai.

## Test
```bash
python -m unittest discover tests
python main.py --version
```
