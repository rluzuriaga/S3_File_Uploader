from S3_File_Uploader.Database import Database

with Database() as DB:
    DB_VERSION = DB.get_db_version()

APP_TITLE = "S3 File Uploader"
APP_VERSION = "0.3"
