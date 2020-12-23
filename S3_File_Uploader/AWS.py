import logging

import boto3
import botocore

from S3_File_Uploader.Database import Database

logger = logging.getLogger('main_logger')


class AWS:
    # def __init__(self):
    #     pass

    @staticmethod
    def test_connection(aws_access_key_id, aws_secret_access_key, region_code):
        logger.debug(f'Testing AWS connection.')

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
                logger.warning(f'Raising AWSKeyException.')

                raise AWSKeyException
        except botocore.exceptions.EndpointConnectionError:
            logger.warning(f'Raising NoConnectionError')

            raise NoConnectionError

        logger.debug(f'Connection successful.')

    @staticmethod
    def get_s3_buckets():
        with Database() as DB:
            if DB.are_settings_saved():
                # try:
                aws_config = DB.get_aws_config()
                client = boto3.client(
                    's3',
                    aws_access_key_id=aws_config[0],
                    aws_secret_access_key=aws_config[1],
                    region_name=aws_config[2]
                )

                buckets_dict = client.list_buckets()

                buckets_values = tuple(bucket_name['Name'] for bucket_name in buckets_dict['Buckets'])

                logger.debug(f'Retrieving all S3 buckets.')

                return buckets_values

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

            logger.debug(f'Uploading file to S3.')

            client.upload_file(file_path, bucket_name, file_name,
                               Callback=ProgressCallback)

    @staticmethod
    def create_single_folder_in_bucket(bucket_name, folder_name):
        with Database() as DB:
            aws_config = DB.get_aws_config()

            client = boto3.client(
                's3',
                aws_access_key_id=aws_config[0],
                aws_secret_access_key=aws_config[1],
                region_name=aws_config[2]
            )

            logger.debug(f'Creating folder in S3 Bucket.')

            client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))

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

            logger.debug(f'Creating multiple folders in the S3 Bucket.')

            for folder_name in list_of_folder_names:
                if folder_name + '/' not in bucket_objects_dict:
                    client.put_object(Bucket=bucket_name,
                                      Key=(folder_name+'/'))

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

            logger.debug(f'Retrieving S3 Bucket objects as a dictionary.')

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
