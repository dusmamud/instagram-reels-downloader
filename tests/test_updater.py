import json
import unittest
from unittest.mock import MagicMock, patch

from reels_dl.utils.updater import check_for_updates, parse_version


class TestUpdater(unittest.TestCase):
    def test_parse_version(self):
        self.assertEqual(parse_version("1.2.0"), (1, 2, 0))
        self.assertEqual(parse_version("v1.0.0"), (1, 0, 0))

    def _mock_response(self, version):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({"info": {"version": version}}).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        return mock_response

    @patch("reels_dl.utils.updater.urllib.request.urlopen")
    def test_check_for_updates_available(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response("1.2.0")
        self.assertEqual(check_for_updates(), "1.2.0")

    @patch("reels_dl.utils.updater.urllib.request.urlopen")
    def test_check_for_updates_not_available(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response("1.0.0")
        self.assertIsNone(check_for_updates())

    @patch("reels_dl.utils.updater.urllib.request.urlopen")
    def test_check_for_updates_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection timed out")
        self.assertIsNone(check_for_updates())


if __name__ == "__main__":
    unittest.main()
