from __future__ import annotations

import os
import sqlite3
import logging
from functools import wraps
from typing import Callable, List, Optional, Tuple, Any

from config import DatabasePath, DB_VERSION

logger = logging.getLogger('main_logger')


class Database:
    def __init__(self) -> None:
        logger.info(f'Initializing the database.')

        self.create_db = False
        self.context = False

    def __enter__(self) -> Database:
        logger.info(f'Entering database context.')

        self.context = True

        if not os.path.exists(DatabasePath.get()):
            self.create_db = True

        self.connection = sqlite3.connect(DatabasePath.get())
        self.cursor = self.connection.cursor()

        if self.create_db:
            self.create_database()

        return self

    def __exit__(self, *args: Any) -> None:
        logger.info(f'Exiting database context.')

        del self.cursor

        self.connection.close()
        del self.connection

    def _only_context(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Callable:
            if not self.context:
                raise NotWithContext(
                    "Database should only be used as a context manager. Call it by using 'with Database()'.")
            return func(self, *args, **kwargs)
        return wrapper

    @_only_context
    def create_database(self) -> None:
        logger.debug(f'Creating database.')

        self.cursor.executescript(
            f'''
            CREATE TABLE IF NOT EXISTS aws_regions (
                region_name_text text PRIMARY KEY,
                region_code text NOT NULL
            );
            
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('US East (Ohio)', 'us-east-2');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('US East (N. Virginia)', 'us-east-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('US West (N. California)', 'us-west-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('US West (Oregon)', 'us-west-2');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Africa (Cape Town)', 'af-south-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Hong Kong)', 'ap-east-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Mumbai)', 'ap-south-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Osaka-Local)', 'ap-northeast-3');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Seoul)', 'ap-northeast-2');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Singapore)', 'ap-southeast-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Sydney)', 'ap-southeast-2');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Asia Pacific (Tokyo)', 'ap-northeast-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Canada (Central)', 'ca-central-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('China (Beijing)', 'cn-north-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('China (Ningxia)', 'cn-northwest-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Europe (Frankfurt)', 'eu-central-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Europe (Ireland)', 'eu-west-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Europe (London)', 'eu-west-2');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Europe (Milan)', 'eu-south-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Europe (Paris)', 'eu-west-3');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Europe (Stockholm)', 'eu-north-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('Middle East (Bahrain)', 'me-south-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('South America (São Paulo)', 'sa-east-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('AWS GovCloud (US-East)', 'us-gov-east-1');
            INSERT INTO aws_regions (region_name_text, region_code) VALUES ('AWS GovCloud (US)', 'us-gov-west-1');
            

            CREATE TABLE IF NOT EXISTS aws_config (
                aws_access_key_id text NOT NULL,
                aws_secret_access_key text NOT NULL,
                region text NOT NULL,
                output text NOT NULL,
                is_active integer NOT NULL,
                UNIQUE (aws_access_key_id, aws_secret_access_key)
            );

            CREATE TABLE IF NOT EXISTS ffmpeg_config (
                ffmpeg_parameters text,
                file_suffix TEXT NOT NULL,
                aws_different_output_extension text,
                local_save_path text,
                local_different_output_extension text,
                is_active integer NOT NULL
            );

            CREATE TABLE IF NOT EXISTS mass_upload (
                upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
                aws_secret_access_key text NOT NULL,
                start_date_time text NOT NULL,
                mass_upload_path text NOT NULL,
                s3_bucket text NOT NULL,
                upload_type text NOT NULL,
                use_ffmpeg integer NOT NULL,
                is_done integer NOT NULL,
                finish_date_time text,

                FOREIGN KEY (aws_secret_access_key)
                REFERENCES aws_config (aws_secret_access_key)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS file_upload (
                file_path text NOT NULL,
                file_name text NOT NULL,
                upload_id INTEGER NOT NULL,
                s3_bucket text NOT NULL,
                file_size_bytes INTEGER NOT NULL,
                start_date_time text NOT NULL,
                finish_date_time text,

                FOREIGN KEY (upload_id)
                REFERENCES mass_upload (upload_id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
                
                FOREIGN KEY (s3_bucket)
                REFERENCES mass_upload (s3_bucket)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS ffmpeg_file_conversion (
                original_file_path TEXT NOT NULL,
                original_file_name TEXT NOT NULL,
                original_file_size INTEGER NOT NULL,
                converted_file_path	TEXT NOT NULL,
                converted_file_name	TEXT NOT NULL,
                converted_file_size	INTEGER NOT NULL,
                converted_date_time	INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS file_extensions (
                type_of_file text NOT NULL,
                general_file_extension text NOT NULL,
                file_extension text NOT NULL
            );

            CREATE TABLE IF NOT EXISTS versioning (
                db_version INTEGER NOT NULL
            );

            INSERT INTO versioning (db_version) VALUES ({DB_VERSION});

            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'mp4');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4a');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4v');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'f4v');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'f4a');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4b');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4r');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'f4b');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'mov');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'mkv');

            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', '3GP', '3gp');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', '3GP', '3gp2');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', '3GP', '3g2');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', '3GP', '3gpp');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', '3GP', '3gpp2');

            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'OGG', 'ogg');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'OGG', 'oga');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'OGG', 'ogv');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'OGG', 'ogx');
            
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'WMV', 'wmv');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'WMV', 'wma');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'WMV', 'asf');

            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'WEBM', 'webm');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'FLV', 'flv');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'AVI', 'avi');
            '''
        )

        self.connection.commit()
        logger.debug(f'Commiting database creation.')

    @_only_context
    def update_database_with_sql_file(self, sql_file: str) -> None:
        """ Function to use when trying to update the database using an SQL file.

        Args:
            sql_file (str): The full file path to where the SQL file is downloaded on the computer.
        """

        logger.debug(f'Opening the sql file to set as string.')
        sql_as_string = open(sql_file).read()

        logger.debug(f'Executing SQL file as script.')
        self.cursor.executescript(sql_as_string)

        logger.debug(f'Commiting database with new changes.')
        self.connection.commit()

    @_only_context
    def add_mass_upload_data(self, mass_upload_path: str, s3_bucket: str, upload_type: str, use_ffmpeg: int) -> None:
        logger.debug(f'Adding mass upload data to database.')

        secret_key = self.cursor.execute(
            'SELECT aws_secret_access_key FROM aws_config WHERE is_active = 1;').fetchone()[0]

        self.cursor.execute(
            f'''
            INSERT INTO mass_upload (aws_secret_access_key, start_date_time, mass_upload_path, s3_bucket, upload_type, use_ffmpeg, is_done, finish_date_time)
            VALUES ('{secret_key}', datetime('now', 'localtime'), '{mass_upload_path}', '{s3_bucket}', '{upload_type}', {use_ffmpeg}, 0, NULL);
            '''
        )
        logger.debug(
            f'Inserting `mass_upload_path={mass_upload_path}`, `s3_bucket={s3_bucket}`, `upload_type={upload_type}`, `use_ffmpeg={use_ffmpeg}`')

        self.connection.commit()
        logger.debug(f'Commiting database insertion.')

    @_only_context
    def finish_mass_upload(self) -> None:
        logger.debug(f'Updating mass upload table with finish_date_time.')

        self.cursor.execute(
            """
            UPDATE mass_upload
            SET is_done = 1, finish_date_time = datetime('now', 'localtime')
            WHERE is_done = 0;
            """
        )

        self.connection.commit()
        logger.debug(f'Commiting database update.')

    @_only_context
    def get_region_name_code(self, region_name: str) -> str:
        output = self.cursor.execute(
            f'''
            SELECT region_code 
            FROM aws_regions 
            WHERE region_name_text = '{region_name}';
            '''
        ).fetchone()[0]

        logger.debug(f'Returning region code `{output}` from region name `{region_name}`')

        return output

    @_only_context
    def get_region_name_labels(self) -> Tuple[str, ...]:
        output = self.cursor.execute(
            '''
            SELECT region_name_text
            FROM aws_regions;
            '''
        ).fetchall()

        output_tuple = tuple(a[0] for a in output)

        logger.debug(f'Returning all region name labels as a tuple: `{output_tuple}`')

        return output_tuple

    @_only_context
    def get_aws_config(self, label: bool = False) -> Tuple[str, ...]:
        if label:
            output = self.cursor.execute(
                '''
                SELECT a.aws_access_key_id, a.aws_secret_access_key, r.region_name_text
                FROM aws_config a
                INNER JOIN aws_regions r 
                ON a.region = r.region_code
                WHERE a.is_active = 1;
                '''
            ).fetchone()

            logger.debug(f'Returning AWS config labels `{output}`')
        else:
            output = self.cursor.execute(
                '''
                SELECT aws_access_key_id, aws_secret_access_key, region, output
                FROM aws_config
                WHERE is_active = 1;
                '''
            ).fetchone()

            logger.debug(f'Returning AWS config `{output}`')

        return output

    @_only_context
    def set_aws_config(self, access_key_id: str, secret_key: str, region_name_code: str) -> None:
        # Check if currect saved setting is the same as new one,
        # If so then nothing is changed
        # If they are different, then the old setting will change `is_active` to false
        output = self.cursor.execute(
            '''
            SELECT aws_access_key_id, aws_secret_access_key, region
            FROM aws_config
            WHERE is_active = 1;
            '''
        ).fetchone()

        if output is None:
            pass
        else:
            if access_key_id == output[0] and secret_key == output[1] and region_name_code == output[2]:
                return
            else:
                self.cursor.execute(
                    'UPDATE aws_config SET is_active = 0 WHERE is_active = 1;')

        # Insert new config data
        try:
            self.cursor.execute(
                f'''
                INSERT INTO aws_config (aws_access_key_id, aws_secret_access_key, region, output, is_active)
                VALUES ('{access_key_id}', '{secret_key}', '{region_name_code}', 'json', 1);
                '''
            )
        except sqlite3.IntegrityError:
            self.cursor.execute(
                f'''
                UPDATE aws_config
                SET is_active = 1, region = '{region_name_code}'
                WHERE aws_access_key_id = '{access_key_id}'
                AND aws_secret_access_key = '{secret_key}';
                '''
            )

        logger.debug(f'Setting AWS config on database.')

        self.connection.commit()
        logger.debug(f'Commiting database.')

    @_only_context
    def make_aws_config_inactive(self) -> None:
        self.cursor.execute("Update aws_config SET is_active = 0 WHERE is_active = 1;")
        logger.debug(f'Setting saved AWS config to not active.')

        self.connection.commit()
        logger.debug(f'Commiting database.')

    @_only_context
    def are_settings_saved(self) -> bool:
        logger.debug(f'Checking if settings are saved on the database.')

        if self.get_aws_config() is None:
            return False

        if self.get_ffmpeg_config() is None:
            return False

        return True

    @_only_context
    def get_ffmpeg_config(self) -> Tuple[Optional[str], ...]:
        try:
            output = self.cursor.execute(
                '''
                SELECT ffmpeg_parameters, file_suffix, aws_different_output_extension, local_save_path, local_different_output_extension
                FROM ffmpeg_config 
                WHERE is_active = 1;
                '''
            ).fetchone()

            logger.debug(f'Retrieving ffmpeg config `{output}`')
        except sqlite3.OperationalError as e:
            logger.error(f'ERROR: {e}')

            if "no such column: file_suffix" in str(e):
                logger.warning(f'Database schema out of date.')
                output = self.cursor.execute(
                    '''
                    SELECT ffmpeg_parameters, '_converted', aws_different_output_extension, local_save_path, local_different_output_extension
                    FROM ffmpeg_config 
                    WHERE is_active = 1;
                    '''
                ).fetchone()

                logger.debug(f'Retrieving ffmpeg config `{output}`')

        return output

    @_only_context
    def set_ffmpeg_config(self, ffmpeg_parameters: str,
                          file_suffix: str, aws_different_output_extension: str,
                          local_save_path: str, local_different_output_extension: str) -> None:

        # TODO: check why this prints a string in a string    print(aws_different_output_extension)

        output = self.cursor.execute(
            '''
            SELECT ffmpeg_parameters, file_suffix, aws_different_output_extension, local_save_path, local_different_output_extension
            FROM ffmpeg_config
            WHERE is_active = 1;
            '''
        ).fetchone()

        if output is None:
            pass
        else:
            if ffmpeg_parameters == output[0] and file_suffix == output[1] and aws_different_output_extension == output[2] and local_save_path == output[3] and local_different_output_extension == output[4]:
                return
            else:
                self.cursor.execute(
                    'UPDATE ffmpeg_config SET is_active = 0 WHERE is_active = 1;')

        # Insert new config data
        self.cursor.execute(
            f'''
            INSERT INTO ffmpeg_config (ffmpeg_parameters, file_suffix, aws_different_output_extension, local_save_path, local_different_output_extension, is_active)
            VALUES ('{ffmpeg_parameters}', '{file_suffix}', {aws_different_output_extension}, {local_save_path}, {local_different_output_extension}, 1);
            '''
        )

        logger.debug(f'Setting ffmpeg config on the database.')

        self.connection.commit()
        logger.debug(f'Commiting database.')

    @_only_context
    def get_video_formats(self, labels: bool = False, general_file_ext: Optional[str] = None) -> List[str]:
        if labels:
            output = self.cursor.execute(
                '''
                SELECT DISTINCT general_file_extension
                FROM file_extensions
                WHERE type_of_file = 'video';
                '''
            ).fetchall()

            logger.debug(f'Retriving video format labels.')

        else:
            output = self.cursor.execute(
                f'''
                SELECT file_extension
                FROM file_extensions
                WHERE type_of_file = 'video'
                AND general_file_extension = '{general_file_ext}';
                '''
            ).fetchall()

            logger.debug(f'Retrieving the video format extensions.')

        # The output is a list of tuples, but the tuples are just one string
        # So converting the output to just be a list with the labels (this avoids nested loops)
        output_ = [val[0] for val in output]

        return output_

    @_only_context
    def get_mass_upload_not_ended_data(self) -> List[Optional[Tuple[int, str, str, str, int]]]:
        output = self.cursor.execute(
            '''
            SELECT upload_id, mass_upload_path, s3_bucket, upload_type, use_ffmpeg
            FROM mass_upload
            WHERE is_done = 0;
            '''
        ).fetchall()

        logger.debug(f'Retrieving data from mass upload that is not finished.')

        return output

    @_only_context
    def add_file_upload(self, file_path: str, file_name: str,
                        file_size: int, s3_bucket: str) -> None:
        logger.debug(f'Adding file upload data to database.')

        output = self.cursor.execute(
            """
            SELECT upload_id
            FROM mass_upload
            WHERE is_done = 0;
            """
        ).fetchall()

        if type(output[0]) is int:
            upload_id = output[0]
        else:
            upload_id = output[0][0]

        self.cursor.execute(
            f"""
            INSERT INTO file_upload (file_path, file_name, upload_id, s3_bucket, file_size_bytes, start_date_time, finish_date_time)
            VALUES ('{file_path}', '{file_name}', {upload_id}, '{s3_bucket}', {file_size}, datetime('now', 'localtime'), NULL);
            """
        )

        self.connection.commit()
        logger.debug(f'Commiting database.')

    @_only_context
    def finish_file_upload(self, file_path: str, file_name: str) -> None:
        self.cursor.execute(
            f"""
            UPDATE file_upload
            SET finish_date_time = datetime('now', 'localtime')
            WHERE file_path = '{file_path}'
            AND file_name = '{file_name}';
            """
        )

        logger.debug(f'Finalizing file upload.')

        self.connection.commit()
        logger.debug(f'Commiting database.')

    @_only_context
    def get_file_upload_size(self, file_path: str, file_name: str) -> int:
        output = self.cursor.execute(
            f'''
            SELECT file_size_bytes
            FROM file_upload
            WHERE file_path = '{file_path}'
            AND file_name = '{file_name}';
            '''
        ).fetchone()

        if output:
            if type(output[0]) is int:
                file_size = output[0]
            else:
                file_size = output[0][0]
        else:
            file_size = 0

        logger.debug(f'Retrieving file upload size: `file_size={file_size}`')

        return file_size

    @_only_context
    def add_ffmpeg_conversion(self, original_file_path: str, original_file_name: str, original_file_size: str,
                              converted_file_path: str, converted_file_name: str, converted_file_size: str) -> None:

        self.cursor.execute(
            f'''
            INSERT INTO ffmpeg_file_conversion (
                original_file_path, original_file_name, original_file_size,
                converted_file_path, converted_file_name, converted_file_size, converted_date_time
            )
            VALUES (
                '{original_file_path}', '{original_file_name}', '{original_file_size}',
                '{converted_file_path}', '{converted_file_name}', '{converted_file_size}',
                datetime('now', 'localtime')
            );
            '''
        )

        logger.debug(f'Inserting ffmpeg file conversion data.')

        self.connection.commit()
        logger.debug(f'Commiting database.')

    @_only_context
    def is_file_already_converted_and_uploaded(self, file_path: str, file_name: str,
                                               file_size: int, s3_bucket: str) -> bool:
        output = self.cursor.execute(
            f'''
            SELECT c.original_file_path, c.original_file_name, c.original_file_size, 
                   c.converted_file_path, c.converted_file_name, c.converted_file_size,
                   f.file_path, f.file_name, f.file_size_bytes

            FROM ffmpeg_file_conversion c

            INNER JOIN file_upload f ON c.converted_file_size = f.file_size_bytes

            WHERE f.s3_bucket = '{s3_bucket}'
            AND c.original_file_path = '{file_path}'
            AND c.original_file_name = '{file_name}'
            AND c.original_file_size = '{file_size}'
            AND f.file_path = c.converted_file_path
            AND f.file_name = c.converted_file_name
            AND f.file_size_bytes = c.converted_file_size;
            '''
        ).fetchall()

        logger.debug(f'Checking if a file is already converted and uploaded.')

        return bool(output)

    @_only_context
    def get_tests_table(self) -> Optional[Tuple[str]]:
        logger.debug(f'Trying to retrieve everyting from the tests table.')
        try:
            output = self.cursor.execute('SELECT * FROM tests;').fetchone()
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                output = None
            else:
                raise sqlite3.OperationalError(str(e))

        return output


class NotWithContext(Exception):
    pass
