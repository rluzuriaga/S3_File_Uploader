from functools import wraps
import sqlite3
import os


class Database:
    def __init__(self, custom_db_path=None):
        self.create_db = False
        self.context = False
        self.db_path = custom_db_path

        if custom_db_path == None:
            self.db_path = os.getcwd() + "/db.sqlite3"

    def __enter__(self):
        self.context = True

        if not os.path.exists(self.db_path):
            self.create_db = True

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        if self.create_db:
            self.create_database()

        return self

    def __exit__(self, type, value, traceback):
        del self.cursor

        self.connection.close()
        del self.connection

    def _only_context(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.context:
                raise NotWithContext(
                    "Database should only be used as a context manager. Call it by using 'with Database()'.")
            return func(self, *args, **kwargs)
        return wrapper

    @_only_context
    def create_database(self):
        self.cursor.executescript(
            '''
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
                start_date_time text NOT NULL,
                finish_date_time text,

                FOREIGN KEY (upload_id)
                REFERENCES mass_upload (upload_id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS file_extensions (
                type_of_file text NOT NULL,
                general_file_extension text NOT NULL,
                file_extension text NOT NULL
            );

            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'mp4');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4a');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4v');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'f4v');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'f4a');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4b');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'm4r');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'f4b');
            INSERT INTO file_extensions (type_of_file, general_file_extension, file_extension) VALUES ('video', 'MP4', 'mov');

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

    @_only_context
    def add_mass_upload_data(self, mass_upload_path, s3_bucket, upload_type):
        secret_key = self.cursor.execute(
            'SELECT aws_secret_access_key FROM aws_config WHERE is_active = 1;').fetchone()[0]

        self.cursor.execute(
            f'''
            INSERT INTO mass_upload (aws_secret_access_key, start_date_time, mass_upload_path, s3_bucket, upload_type, is_done, finish_date_time)
            VALUES ('{secret_key}', datetime('now', 'localtime'), '{mass_upload_path}', '{s3_bucket}', '{upload_type}', 0, NULL);
            '''
        )

        self.connection.commit()

    @_only_context
    def finish_mass_upload(self):
        self.cursor.execute(
            """
            UPDATE mass_upload
            SET is_done = 1, finish_date_time = datetime('now', 'localtime')
            WHERE is_done = 0;
            """
        )

        self.connection.commit()

    @_only_context
    def get_region_name_code(self, region_name):
        output = self.cursor.execute(
            f'''
            SELECT region_code 
            FROM aws_regions 
            WHERE region_name_text = '{region_name}';
            '''
        ).fetchone()[0]

        return output

    @_only_context
    def get_region_name_labels(self):
        output = self.cursor.execute(
            '''
            SELECT region_name_text
            FROM aws_regions;
            '''
        ).fetchall()

        output_tuple = tuple(a[0] for a in output)

        return output_tuple

    @_only_context
    def get_aws_config(self, label=False):
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
        else:
            output = self.cursor.execute(
                '''
                SELECT aws_access_key_id, aws_secret_access_key, region, output FROM aws_config WHERE is_active = 1;
                '''
            ).fetchone()

        return output

    @_only_context
    def set_aws_config(self, access_key_id, secret_key, region_name_code):
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

        self.connection.commit()

    @_only_context
    def are_settings_saved(self):
        if self.get_aws_config() is None:
            return False

        if self.get_ffmpeg_config() is None:
            return False

        return True

    @_only_context
    def get_ffmpeg_config(self):
        output = self.cursor.execute(
            '''
            SELECT ffmpeg_parameters, aws_different_output_extension, local_save_path, local_different_output_extension
            FROM ffmpeg_config 
            WHERE is_active = 1;
            '''
        ).fetchone()

        return output

    @_only_context
    def set_ffmpeg_config(self, ffmpeg_parameters, aws_different_output_extension, local_save_path, local_different_output_extension):
        output = self.cursor.execute(
            '''
            SELECT ffmpeg_parameters, aws_different_output_extension, local_save_path, local_different_output_extension
            FROM ffmpeg_config
            WHERE is_active = 1;
            '''
        ).fetchone()

        if output is None:
            pass
        else:
            if ffmpeg_parameters == output[0] and aws_different_output_extension == output[1] and local_save_path == output[2] and local_different_output_extension == output[3]:
                return
            else:
                self.cursor.execute(
                    'UPDATE ffmpeg_config SET is_active = 0 WHERE is_active = 1;')

        # Insert new config data
        self.cursor.execute(
            f'''
            INSERT INTO ffmpeg_config (ffmpeg_parameters, aws_different_output_extension, local_save_path, local_different_output_extension, is_active)
            VALUES ('{ffmpeg_parameters}', {aws_different_output_extension}, {local_save_path}, {local_different_output_extension}, 1);
            '''
        )

        self.connection.commit()

    @_only_context
    def get_video_formats(self, labels=False, general_file_ext=None):
        if labels:
            output = self.cursor.execute(
                '''
                SELECT DISTINCT general_file_extension
                FROM file_extensions
                WHERE type_of_file = 'video';
                '''
            ).fetchall()
        else:
            output = self.cursor.execute(
                f'''
                SELECT file_extension
                FROM file_extensions
                WHERE type_of_file = 'video'
                AND general_file_extension = '{general_file_ext}';
                '''
            ).fetchall()

        # The output is a list of tuples, but the tuples are just one string
        # So converting the output to just be a list with the labels (this avoids nested loops)
        output_ = [val[0] for val in output]

        return output_

    @_only_context
    def get_mass_upload_not_ended_data(self):
        output = self.cursor.execute(
            '''
            SELECT upload_id, mass_upload_path, s3_bucket, upload_type
            FROM mass_upload
            WHERE is_done = 0;
            '''
        ).fetchall()

        return output

    @_only_context
    def add_file_upload(self, file_path, file_name):
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
            INSERT INTO file_upload (file_path, file_name, upload_id, start_date_time, finish_date_time)
            VALUES ('{file_path}', '{file_name}', {upload_id}, datetime('now', 'localtime'), NULL);
            """
        )

        self.connection.commit()

    @_only_context
    def finish_file_upload(self, file_path, file_name):
        self.cursor.execute(
            f"""
            UPDATE file_upload
            SET finish_date_time = datetime('now', 'localtime')
            WHERE file_path = '{file_path}'
            AND file_name = '{file_name}';
            """
        )

        self.connection.commit()


class NotWithContext(Exception):
    pass
