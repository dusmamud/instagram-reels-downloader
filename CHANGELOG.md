# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-10-30

Initial public release, built in the same style as youtube-music-downloader.

### Added
- Instagram Reels downloader CLI (`dus-ig-reels-dl`, `ig-reels-dl`) and `python main.py` launcher
- Interactive mode: URL, quality, format and login mode step-by-step
- Quality selection: best, 1080p, 720p, 480p (real yt-dlp format selectors)
- Formats: MP4 (default) and WebM, merged video + audio via FFmpeg
- Multiple URLs on the command line and `--batch-file` (one URL per line, `#` comments ignored)
- `--dry-run` (real yt-dlp metadata check, no file written) and `--list-formats`
- Login support: `--browser firefox/chrome/edge/brave` and `--cookies cookies.txt`
- Filename styles: clean (`Uploader-Title-ID.mp4`) and formal (`Uploader - Title [ID].mp4`)
- Progress bar, retries with backoff for 429 / network glitches, partial-file cleanup
- PyPI update check (`check_for_updates`) with a fail-safe 1.5s timeout
- Thumbnail embedding option (`--thumbnail`) and metadata postprocessor
- Unit tests for CLI parsing, quality mapping, URL detection, filename formatting,
  updater, cleanup and config (16 tests, all passing at release check)
- Docs: README, USAGE, INSTALLATION, TROUBLESHOOTING, TEST_GUIDE
- Repo files: LICENSE (MIT), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, DISCLAIMER
- GitHub: CI workflow (Python 3.10/3.11/3.12 on Ubuntu + Windows), PyPI publish
  workflow, issue/PR templates, Dependabot

### Notes
- No mock / placeholder download: every download goes through yt-dlp + FFmpeg.
- Only download your own content, or content you have permission / a Creative
  Commons licence for. See DISCLAIMER.md.
