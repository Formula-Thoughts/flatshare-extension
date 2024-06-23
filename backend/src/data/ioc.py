import os

import boto3

from src.core import IBlobRepo, Group, IGroupRepo, IUserGroupsRepo
from src.data import S3ClientWrapper, CognitoClientWrapper, DynamoDbWrapper, ObjectHasher
from src.data.repositories import S3BlobRepo, S3GroupRepo, S3UserGroupsRepo, DynamoDbUserGroupsRepo
from formula_thoughts_web.ioc import Container

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
dynamo = boto3.resource('dynamodb')


def register_data_dependencies(container: Container):
    (container.register_factory(service=S3ClientWrapper, factory=lambda: S3ClientWrapper(client=s3))
     .register_factory(service=CognitoClientWrapper, factory=lambda: CognitoClientWrapper(client=cognito))
     .register_factory(service=DynamoDbWrapper, factory=lambda: DynamoDbWrapper(tablename=os.environ['DYNAMODB_TABLE'], dynamo_client=dynamo))
     .register(service=ObjectHasher)
     .register(service=IBlobRepo, implementation=S3BlobRepo)
     .register(service=IGroupRepo, implementation=S3GroupRepo)
     .register(service=IUserGroupsRepo, implementation=DynamoDbUserGroupsRepo))
