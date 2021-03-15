import os
import sys
import logging
from datetime import datetime
from typing import Dict, Optional

import requests

from S3_File_Uploader.UI.ProgramController import ProgramController
from S3_File_Uploader.UI.UpdateApp import UpdateApp
from S3_File_Uploader.Database import Database

from config import APP_VERSION, DB_VERSION, LOGS_DIRECTORY


RequestsResponseAlias = Optional[Dict]


# Set up file based logger
current_datetime = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
log_file_path = os.path.join(LOGS_DIRECTORY, f'{current_datetime}.log')

# Check if a logs directory is created, if not then it is created.
if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY)

# Changed the setup of the logger from the basicConfig so that the file isn't logging the imported modules
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_file_path)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


logger.debug(f'Logger setup.')


def request_data_from_gist() -> RequestsResponseAlias:
    logger.debug(f'Retrieving response from gist.')

    header = {"Accept": "application/vnd.github.v3+json"}
    url = "https://api.github.com/gists/d052b99ca4eab941fff359810aa16ff7"

    try:
        response = requests.get(
            url,
            headers=header
        ).json()
    except requests.exceptions.ConnectionError:
        # TODO: need to let user know that there is no network connected
        return None

    return response


def check_app_version(response: RequestsResponseAlias) -> None:
    logger.debug(f'Checking if app version is out of date.')
    try:
        newest_app_version = response['files']['app_version.txt']['content']
    except TypeError:
        # TODO: need to let user know that there is no network connected
        return

    if APP_VERSION == newest_app_version:
        logger.debug(f'App version is up to date.')
        return
    elif float(APP_VERSION) > float(newest_app_version):
        logger.debug(f'App version newer than what is on gist.')
        return
    else:
        logger.debug(f'App version is out of date.')
        UpdateApp()
        sys.exit(0)


def database_updater(response: RequestsResponseAlias) -> None:
    logger.debug(f'Starting database updater.')
    try:
        newest_db_version = response['files']['db_version.txt']['content']
    except TypeError:
        # TODO: need to let user know that there is no network connected
        return

    if newest_db_version != DB_VERSION:
        for i in range(int(DB_VERSION) + 1, int(newest_db_version) + 1):
            sql_file_name = f'db_update_{str(i)}.sql'
            sql_file_url = response['files'][sql_file_name]['raw_url']
            r = requests.get(sql_file_url)
            open(sql_file_name, 'wb').write(r.content)

            with Database() as DB:
                DB.update_database_with_sql_file(sql_file_name)

            os.remove(sql_file_name)


def main() -> None:
    logger.debug(f'Starting program.')

    pc = ProgramController()
    pc.mainloop()

    logger.debug(f'Exiting program.')


if __name__ == "__main__":
    response = request_data_from_gist()
    check_app_version(response)
    database_updater(response)
    main()
