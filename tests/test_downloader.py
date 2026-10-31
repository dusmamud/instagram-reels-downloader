import tempfile
import unittest
from pathlib import Path

from reels_dl.cli import create_parser
from reels_dl.core.downloader import IgReelsDownloader, is_instagram_url, quality_format_spec


class TestReelsDownloader(unittest.TestCase):
    def test_instagram_url_detection(self):
        self.assertTrue(is_instagram_url("https://www.instagram.com/reel/ABC123/"))
        self.assertTrue(is_instagram_url("https://www.instagram.com/reels/ABC123/"))
        self.assertTrue(is_instagram_url("https://www.instagram.com/p/ABC123/"))
        self.assertFalse(is_instagram_url("https://www.youtube.com/watch?v=abc"))
        self.assertFalse(is_instagram_url("https://example.com/reel/123"))

    def test_quality_format_spec(self):
        self.assertEqual(quality_format_spec("best"), "bv*+ba/best")
        self.assertEqual(quality_format_spec("1080"), "bv[height<=1080]+ba/best")
        self.assertEqual(quality_format_spec("720"), "bv[height<=720]+ba/best")
        self.assertEqual(quality_format_spec("480"), "bv[height<=480]+ba/best")

    def test_cli_parser(self):
        parser = create_parser()
        args = parser.parse_args(["https://www.instagram.com/reel/ABC123/", "-q", "720", "-f", "mp4"])
        self.assertEqual(args.quality, "720")
        self.assertEqual(args.format, "mp4")
        args_dry = parser.parse_args(["https://www.instagram.com/reel/ABC123/", "--dry-run"])
        self.assertTrue(args_dry.dry_run)

    def test_dry_run_opts_do_not_download(self):
        dl = IgReelsDownloader(
            output_dir=str(Path(tempfile.gettempdir()) / "ig-reels-test"),
            quality="720",
            dry_run=True,
        )
        opts = dl._build_ydl_opts()
        self.assertTrue(opts["simulate"])
        self.assertIn("720", opts["format"])
        self.assertEqual(opts["merge_output_format"], "mp4")

    def test_cookiefile_auth_wiring(self):
        cookiefile = str(Path(tempfile.gettempdir()) / "cookies.txt")
        dl = IgReelsDownloader(
            output_dir=str(Path(tempfile.gettempdir()) / "ig-reels-test"),
            cookiefile=cookiefile,
        )
        opts = dl._build_ydl_opts()
        self.assertEqual(opts["cookiefile"], cookiefile)


if __name__ == "__main__":
    unittest.main()
