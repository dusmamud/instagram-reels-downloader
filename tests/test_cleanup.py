import tempfile
import unittest
from pathlib import Path

from reels_dl.utils.cleanup import cleanup_partial_files


class TestCleanup(unittest.TestCase):
    def test_cleanup_removes_partial_files_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "a.mp4.part").write_text("x")
            (folder / "b.ytdl").write_text("x")
            (folder / "keep.mp4").write_text("x")
            removed = cleanup_partial_files(folder)
            self.assertEqual(removed, 2)
            self.assertFalse((folder / "a.mp4.part").exists())
            self.assertTrue((folder / "keep.mp4").exists())

    def test_cleanup_missing_folder_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "does-not-exist-ig-reels-test"
            self.assertFalse(missing.exists())
            self.assertEqual(cleanup_partial_files(missing), 0)


if __name__ == "__main__":
    unittest.main()
