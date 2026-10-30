# Test Guide

## What is tested (no network needed for unit tests)
- `tests/test_downloader.py`: Instagram URL detection, quality -> yt-dlp format
  mapping, CLI parsing, dry-run options (`simulate=True`), cookiefile wiring.
- `tests/test_formatters.py`: illegal-character removal, clean and formal filenames.
- `tests/test_config.py`: default download folder, `IG_REELS_DOWNLOAD_DIR` override.
- `tests/test_updater.py`: PyPI version comparison with a mocked HTTP response
  (newer version found, no newer version, network error -> None).
- `tests/test_cleanup.py`: dummy `.part` / `.ytdl` / `.tmp` files are removed by
  `cleanup_partial_files()` in a temporary folder only.

## Running tests
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m unittest discover tests
# or
pytest
```
Configuration is in `pyproject.toml` (`testpaths = ["tests"]`).

## Running one test
```bash
python -m unittest tests.test_downloader.TestReelsDownloader.test_quality_format_spec
python -m unittest tests.test_updater.TestUpdater.test_check_for_updates_available
```

## Live checks (needs network, optional)
Unit tests never download a real reel. For a live check, use your own or a
public, permitted reel and prefer `--dry-run` first:

```bash
python main.py "https://www.instagram.com/reel/REEL_ID/" --dry-run
python main.py "https://www.instagram.com/reel/REEL_ID/" -q 720
```

## Rules for new tests
- Never write into the real `downloads/` folder from a test. Use a temp folder.
- Never use real cookies or real private URLs in tests.
- For network code, mock the HTTP layer (like `test_updater.py` does) instead
  of hitting PyPI or Instagram in a unit test.
- A failing test should fail for a real reason, not because ffmpeg or
  network is missing — unit tests only need Python + the package deps.
