import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from reels_dl import config


class TestConfig(unittest.TestCase):
    def test_env_override(self):
        tmp_dir = Path(tempfile.gettempdir()) / "my-reels"
        with patch.dict(os.environ, {"IG_REELS_DOWNLOAD_DIR": str(tmp_dir)}):
            result = config.get_default_download_dir()
            self.assertEqual(result, tmp_dir.resolve())

    def test_supported_lists(self):
        self.assertIn("mp4", config.SUPPORTED_FORMATS)
        self.assertIn("best", config.SUPPORTED_QUALITIES)
        self.assertIn("1080", config.SUPPORTED_QUALITIES)


if __name__ == "__main__":
    unittest.main()
