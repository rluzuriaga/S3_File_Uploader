import os
import sys


class DatabasePath:
    path = os.path.join(os.getcwd(), 'db.sqlite3')

    @classmethod
    def get(cls) -> str:
        return cls.path

    @classmethod
    def change_path(cls, new_path: str) -> None:
        cls.path = new_path


DB_VERSION = 2

APP_TITLE = "S3 File Uploader"
APP_VERSION = "0.4"

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LOGS_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'logs')

if 'darwin' in sys.platform:
    IS_MAC = True
    IS_WINDOWS = False
elif 'win' in sys.platform:
    IS_WINDOWS = True
    IS_MAC = False
