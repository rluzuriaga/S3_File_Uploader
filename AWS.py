import boto3
import botocore

from Database import Database

class AWS:
    def __init__(self):
        pass

    @staticmethod
    def test_connection(aws_access_key_id, aws_secret_access_key, region_code):
        try:
            client = boto3.client(
                'sts',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_code
            )

            response = client.get_caller_identity()

            return response
        except botocore.exceptions.ClientError as err:
            if 'SignatureDoesNotMatch' in str(err) or 'InvalidClientTokenId' in str(err):
                raise AWSKeyException
        except botocore.exceptions.EndpointConnectionError:
            raise NoConnectionError
    
    @staticmethod
    def get_s3_buckets():
        with Database() as DB:
            if DB.is_aws_config_saved:
                try:
                    aws_config = DB.get_aws_config()
                    client = boto3.client(
                        's3',
                        aws_access_key_id=aws_config[0],
                        aws_secret_access_key=aws_config[1],
                        region_name=aws_config[2]
                    )

                    buckets_dict = client.list_buckets()

                    buckets_values = tuple(bucket_name['Name'] for bucket_name in buckets_dict['Buckets'])

                    return buckets_values
                except Exception:
                    pass

    @staticmethod
    def upload_file(file_path, bucket_name, file_name, ProgressCallback=None):
        with Database() as DB:
            aws_config = DB.get_aws_config()

            client = boto3.client(
                's3',
                aws_access_key_id=aws_config[0],
                aws_secret_access_key=aws_config[1],
                region_name=aws_config[2]
            )

            client.upload_file(file_path, bucket_name, file_name)
            # client.upload_file(file_path, bucket_name, file_name, Callback=ProgressCallback(file_path))

    def create_multiple_folders_in_bucket(self, bucket_name, list_of_folder_names):
        with Database() as DB:
            aws_config = DB.get_aws_config()

            client = boto3.client(
                's3',
                aws_access_key_id=aws_config[0],
                aws_secret_access_key=aws_config[1],
                region_name=aws_config[2]
            )

            bucket_objects_dict = self.get_bucket_objects_as_dict(bucket_name)

            for folder_name in list_of_folder_names:
                if folder_name + '/' not in bucket_objects_dict:
                    client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))
    
    @staticmethod
    def get_bucket_objects_as_dict(bucket_name):
        """ Example output: {'file_name': int(filesize)} """
        with Database() as DB:
            aws_config = DB.get_aws_config()

            client = boto3.client(
                's3',
                aws_access_key_id=aws_config[0],
                aws_secret_access_key=aws_config[1],
                region_name=aws_config[2]
            )

            objects = client.list_objects_v2(Bucket=bucket_name)
            
            try:
                return {item['Key']: item['Size'] for item in objects['Contents']}
            except KeyError:
                return {}


class AWSKeyException(Exception):
    pass

class AWSAuthenticationException(Exception):
    pass

class NoConnectionError(Exception):
    pass