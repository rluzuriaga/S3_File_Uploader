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


class NotWithContext(Exception):
    pass
