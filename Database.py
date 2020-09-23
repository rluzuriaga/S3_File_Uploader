import sqlite3
import os

class Database:
    def __init__(self, custom_db_path=None):
        self.context = False
        self.db_path = custom_db_path

        if custom_db_path == None:
            self.db_path = os.getcwd() + "/db.sqlite3"

    def __enter__(self):
        self.context = True
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def _only_context(func):
        def wrapper(self, *args, **kwargs):
            if not self.context:
                raise NotWithContext("Database should only be used as a context manager. Call it by using 'with Database()'.")
            func(self, *args, **kwargs)
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


class NotWithContext(Exception):
    pass
