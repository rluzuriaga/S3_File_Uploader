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
                raise NotWithContext("Database should only be used as a context manager. Call it by using 'with Database()'.")
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
                output text NOT NULL
            );

            CREATE TABLE IF NOT EXISTS mass_upload (
                upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
                aws_secret_access_key text NOT NULL,
                start_date_time text NOT NULL,
                mass_upload_path text NOT NULL,
                s3_bucket text NOT NULL,
                is_done integer NOT NULL,
                finish_date_time text,

                FOREIGN KEY (aws_secret_access_key)
                REFERENCES aws_config (aws_secret_access_key)
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
    def add_mass_upload_data(self, mass_upload_path, s3_bucket):
        self.cursor.execute(
            f'''
            INSERT INTO mass_upload (start_date_time, mass_upload_path, s3_bucket, is_done, finish_date_time)
            VALUES (datetime('now', 'localtime'), '{mass_upload_path}', '{s3_bucket}', 0, NULL);
            '''
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
    def get_aws_config(self, label=False):
        if label:
            output = self.cursor.execute(
                '''
                SELECT a.aws_access_key_id, a.aws_secret_access_key, r.region_name_text
                FROM aws_config a
                INNER JOIN aws_regions r 
                ON a.region = r.region_code;
                '''
            ).fetchone()
        else:
            output = self.cursor.execute(
                '''
                SELECT aws_access_key_id, aws_secret_access_key, region, output FROM aws_config;
                '''
            ).fetchone()

        return output

    @_only_context
    def set_aws_config(self, access_key_id, secret_key, region_name_code):
        self.cursor.execute('DELETE FROM aws_config WHERE EXISTS (SELECT * FROM aws_config);')
        self.cursor.execute(
            f'''
            INSERT INTO aws_config (aws_access_key_id, aws_secret_access_key, region, output)
            VALUES ('{access_key_id}', '{secret_key}', '{region_name_code}', 'json');
            '''
        )

        self.connection.commit()
    
    @_only_context
    def is_aws_config_saved(self):
        if self.get_aws_config() is None:
            return False
        
        return True
    
    @_only_context
    def get_video_formats(self,labels=False, general_file_ext=None):
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


class NotWithContext(Exception):
    pass
