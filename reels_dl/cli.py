import argparse
import sys
from pathlib import Path

from reels_dl import config
from reels_dl.core.downloader import IgReelsDownloader
from reels_dl.ui.interactive import run_interactive_session
from reels_dl.utils.system import check_dependencies, console, log_error
from reels_dl.version import __version__


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Instagram Reels Downloader CLI & Interactive Studio",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=f"dus-ig-reels-dl {__version__}")
    parser.add_argument("urls", nargs="*", help="Instagram Reel URL(s), e.g. https://www.instagram.com/reel/...")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode (default jab koi URL na ho)")
    parser.add_argument("-f", "--format", choices=config.SUPPORTED_FORMATS, default=config.DEFAULT_FORMAT, help="Video format (default: mp4)")
    parser.add_argument("-q", "--quality", choices=config.SUPPORTED_QUALITIES, default=config.DEFAULT_QUALITY, help="Quality: best, 1080, 720, 480 (default: best)")
    parser.add_argument("-n", "--naming-style", choices=["clean", "formal"], default="clean", help="Filename style (default: clean)")
    parser.add_argument("-F", "--list-formats", action="store_true", help="Sirf available formats dikhao, download mat karo")
    parser.add_argument("--batch-file", default=None, help="Ek text file jisme har line par ek Reel URL ho")
    parser.add_argument("--dry-run", action="store_true", help="Sirf check karo, file save mat karo")
    parser.add_argument("--thumbnail", action="store_true", help="Reel thumbnail ko video me embed karo")
    parser.add_argument("-a", "--auth-mode", choices=["none", "browser", "cookiefile"], default=config.DEFAULT_AUTH_MODE, help="Auth mode (default: none)")
    parser.add_argument("-B", "--browser", default=None, help="Browser for cookies: firefox, chrome, edge, brave")
    parser.add_argument("-C", "--cookies", default=None, help="cookies.txt file ka path")
    parser.add_argument("--no-cookies", action="store_true", help="Bina cookies ke try karo (default hi ye hai)")
    parser.add_argument("-o", "--output", default=None, help=f"Output folder (default: {config.OUTPUT_DIR})")
    return parser


def main():
    try:
        if len(sys.argv) == 1:
            run_interactive_session()
            return
        parser = create_parser()
        args = parser.parse_args()
        if args.output:
            config.set_output_dir(args.output)
        if args.interactive or (not args.urls and not args.batch_file):
            run_interactive_session(output_dir=args.output)
            return
        if not check_dependencies():
            sys.exit(1)

        urls = list(args.urls)
        if args.batch_file:
            batch_path = Path(args.batch_file)
            if not batch_path.exists():
                log_error(f"Batch file nahi mili: {args.batch_file}")
                sys.exit(1)
            urls.extend([line.strip() for line in batch_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")])
        if not urls:
            log_error("Koi URL nahi diya. Ek Reel URL do ya --batch-file use karo.")
            sys.exit(1)

        if args.cookies:
            auth_mode = "cookiefile"
        elif args.browser:
            auth_mode = "browser"
        elif args.no_cookies:
            auth_mode = "none"
        else:
            auth_mode = args.auth_mode

        downloader = IgReelsDownloader(
            output_dir=args.output,
            quality=args.quality,
            video_format=args.format,
            auth_mode=auth_mode,
            browser=args.browser,
            cookiefile=args.cookies,
            dry_run=args.dry_run,
            embed_thumbnail=args.thumbnail,
        )
        if args.list_formats:
            success = downloader.list_formats(urls[0])
            sys.exit(0 if success else 1)
        results = downloader.download_many(urls, naming_style=args.naming_style)
        failed = [r for r in results if not r["success"]]
        sys.exit(1 if failed else 0)
    except (KeyboardInterrupt, EOFError):
        console.print("\n\n[bold yellow]Cancelled by user. Bye![/bold yellow]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
