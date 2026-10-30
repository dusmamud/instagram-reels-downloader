#!/usr/bin/env python3
"""
Instagram Reels Downloader - Root Entry Point Launcher.
Run: python main.py [URL] [options]  (no arguments = interactive mode)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reels_dl.cli import main

if __name__ == "__main__":
    main()
