import boto3
import botocore

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


class AWSKeyException(Exception):
    pass

class AWSAuthenticationException(Exception):
    pass

class NoConnectionError(Exception):
    pass