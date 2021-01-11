import sys
from S3_File_Uploader.Database import Database

with Database() as DB:
    DB_VERSION = DB.get_db_version()

APP_TITLE = "S3 File Uploader"
APP_VERSION = "0.4"

if 'darwin' in sys.platform:
    IS_MAC = True
    IS_WINDOWS = False
elif 'win' in sys.platform:
    IS_WINDOWS = True
    IS_MAC = False
