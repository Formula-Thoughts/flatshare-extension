import os

import boto3
from formula_thoughts_web.ioc import Container

from src.core import IGroupRepo, IUserGroupsRepo, IPropertyRepo
from src.data import CognitoClientWrapper, DynamoDbWrapper, ObjectHasher
from src.data.repositories import DynamoDbUserGroupsRepo, DynamoDbGroupRepo, DynamoDbPropertyRepo

cognito = boto3.client('cognito-idp')
dynamo = boto3.resource('dynamodb')


def register_data_dependencies(container: Container):
    (container.register_factory(service=CognitoClientWrapper, factory=lambda: CognitoClientWrapper(client=cognito))
     .register_factory(service=DynamoDbWrapper,
                       factory=lambda: DynamoDbWrapper(tablename=os.environ['DYNAMODB_TABLE'], dynamo_client=dynamo))
     .register(service=ObjectHasher)
     .register(service=IUserGroupsRepo, implementation=DynamoDbUserGroupsRepo)
     .register(service=IGroupRepo, implementation=DynamoDbGroupRepo)
     .register(service=IPropertyRepo, implementation=DynamoDbPropertyRepo))
