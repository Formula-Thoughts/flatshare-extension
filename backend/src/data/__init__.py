import hashlib

import boto3
from boto3 import dynamodb
from boto3.dynamodb.conditions import Key, Attr
from botocore.client import BaseClient
from formula_thoughts_web.abstractions import Serializer
from formula_thoughts_web.crosscutting import ObjectMapper

CognitoUserPoolId = str

Username = str

S3Key = str

S3Object = str

S3BucketName = str

S3BucketPrefix = str

ContentType = str


CONDITIONAL_CHECK_FAILED = 'ConditionalCheckFailedException'
RESOURCE_NOT_FOUND = 'ResourceNotFoundException'


class ObjectHasher:

    def __init__(self, serializer: Serializer,
                 object_mapper: ObjectMapper):
        self.__object_mapper = object_mapper
        self.__serializer = serializer

    def hash(self, object) -> str:
        dhash = hashlib.md5()
        json = self.__serializer.serialize(data=self.__object_mapper.map_to_dict(_from=object, to=type(object), preserve_decimal=True))
        encoded = json.encode()
        dhash.update(encoded)
        return dhash.hexdigest()


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
        self.__table = dynamo_client.Table(tablename)

    def put(self,
            item: dict,
            condition_expression: boto3.dynamodb.conditions.ConditionBase):
        self.__table.put_item(Item=item,
                              ConditionExpression=condition_expression)

    def update_item(self,
                    key: dict,
                    update_expression: str,
                    condition_expression: boto3.dynamodb.conditions.ConditionBase,
                    expression_attribute_values: dict):
        self.__table.update_item(Key=key,
                                 UpdateExpression=update_expression,
                                 ConditionExpression=condition_expression,
                                 ExpressionAttributeValues=expression_attribute_values)

    def query(self,
              key_condition_expression: boto3.dynamodb.conditions.ConditionBase,
              filter_expression: boto3.dynamodb.conditions.ConditionBase = Attr('id').exists()) -> dict:
        return self.__table.query(KeyConditionExpression=key_condition_expression,
                                  FilterExpression=filter_expression)
