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
    
    def get_s3_buckets(self):
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


class AWSKeyException(Exception):
    pass

class AWSAuthenticationException(Exception):
    pass

class NoConnectionError(Exception):
    pass