import os
import sys


class DatabasePath:
    path: str = os.path.join(os.getcwd(), 'db.sqlite3')

    @classmethod
    def get(cls) -> str:
        return cls.path

    @classmethod
    def change_path(cls, new_path: str) -> None:
        cls.path = new_path


DB_VERSION: int = 2

APP_TITLE: str = "S3 File Uploader"
APP_VERSION: str = "0.4"

WORKING_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'S3_File_Uploader')
LOGS_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'logs')

IS_MAC: bool
IS_WINDOWS: bool

if 'darwin' in sys.platform:
    IS_MAC = True
    IS_WINDOWS = False
elif 'win' in sys.platform:
    IS_WINDOWS = True
    IS_MAC = False
