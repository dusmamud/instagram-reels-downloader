import unittest

from reels_dl.utils.formatters import format_filename, sanitize_name


class TestFormatters(unittest.TestCase):
    def test_sanitize_removes_illegal_chars(self):
        self.assertEqual(sanitize_name('A/B:C*D?"E'), "ABCDE")

    def test_clean_filename(self):
        name = format_filename("Some User", "My Reel Title", "ABC123", "mp4", "clean")
        self.assertEqual(name, "Some-User-My-Reel-Title-ABC123.mp4")

    def test_formal_filename(self):
        name = format_filename("Some User", "My Reel Title", "ABC123", "mp4", "formal")
        self.assertEqual(name, "Some User - My Reel Title [ABC123].mp4")


if __name__ == "__main__":
    unittest.main()
