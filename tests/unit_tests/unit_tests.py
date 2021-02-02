import os
import unittest
from shutil import which

from dotenv import load_dotenv


load_dotenv()


class MainTestCase(unittest.TestCase):
    def test_environ_vars_available(self) -> None:
        """ Test if the environment variables a present. """
        self.assertIsNotNone(os.environ.get('AWS_ACCESS_KEY_ID'))
        self.assertIsNotNone(os.environ.get('AWS_SECRET_KEY'))
        self.assertIsNotNone(os.environ.get('AWS_REGION_NAME'))

    def test_ffmpeg_in_path(self) -> None:
        """ Test if ffmpeg is added to path. """
        self.assertIsNotNone(which('ffmpeg'))

    def test_ffprobe_in_path(self) -> None:
        """ Test if ffprobe is added to path. """
        self.assertIsNotNone(which('ffprobe'))


if __name__ == "__main__":
    unittest.main()
