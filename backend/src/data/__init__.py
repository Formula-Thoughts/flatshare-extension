import boto3
from boto3.dynamodb.conditions import Key
from botocore.client import BaseClient

CognitoUserPoolId = str

Username = str

S3Key = str

S3Object = str

S3BucketName = str

S3BucketPrefix = str

ContentType = str


class S3ClientWrapper:

    def __init__(self, client: BaseClient):
        self.__s3_client = client

    def put_object(self,
                   bucket: S3BucketName,
                   key: S3Key,
                   body: S3Object,
                   content_type: ContentType) -> None:
        self.__s3_client.put_object(Bucket=bucket,
                                    Key=key,
                                    Body=body,
                                    ContentType=content_type)

    def list_objects_v2(self,
                        bucket: S3BucketName,
                        prefix: S3BucketPrefix) -> list[S3Key]:
        return list(map(lambda x: x['Key'], list(self.__s3_client.list_objects_v2(Bucket=bucket,
                                                                                  Prefix=prefix)['Contents'])))

    def get_object(self,
                   bucket: S3BucketName,
                   key: S3Key) -> S3Object:
        return self.__s3_client.get_object(Bucket=bucket,
                                           Key=key)['Body'].read()

    def delete_object(self,
                      bucket: S3BucketName,
                      key: S3Key) -> None:
        self.__s3_client.delete_object(Bucket=bucket,
                                       Key=key)


class CognitoClientWrapper:

    def __init__(self, client: BaseClient):
        self.__cognito_client = client

    def admin_get_user(self,
                       user_pool_id: CognitoUserPoolId,
                       username: Username) -> dict:
        return self.__cognito_client.admin_get_user(UserPoolId=user_pool_id,
                                                    Username=username)


class DynamoDbWrapper:

    def __init__(self, tablename: str,
                 dynamo_client: BaseClient):
        self.__dynamo_client = dynamo_client
        self.__tablename = tablename

    def put(self,
            item: dict,
            condition_expression: boto3.dynamodb.conditions.ConditionBase):
        self.__dynamo_client.put_item(TableName=self.__tablename,
                                      Item=item,
                                      ConditionExpression=condition_expression)

    def update_item(self,
                    key: dict,
                    update_expression: str,
                    condition_expression: boto3.dynamodb.conditions.ConditionBase):
        self.__dynamo_client.update_item(Key=key,
                                         UpdateExpression=update_expression,
                                         ConditionExpression=condition_expression)

    def query(self,
              key_condition_expression: boto3.dynamodb.conditions.ConditionBase):
        self.__dynamo_client.query(KeyConditionExpression=key_condition_expression)
