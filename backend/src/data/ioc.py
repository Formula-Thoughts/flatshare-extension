import os

import boto3
from formula_thoughts_web.ioc import Container

from src.core import IGroupRepo, IUserGroupsRepo, IPropertyRepo, IRedFlagRepo
from src.data import CognitoClientWrapper, DynamoDbWrapper, ObjectHasher
from src.data.repositories import DynamoDbUserGroupsRepo, DynamoDbGroupRepo, DynamoDbPropertyRepo, DynamoDbRedFlagRepo

cognito = boto3.client('cognito-idp', region_name='eu-west-2')
dynamo = boto3.resource('dynamodb', region_name='eu-west-2')


def register_data_dependencies(container: Container):
    (container.register_factory(service=CognitoClientWrapper, factory=lambda: CognitoClientWrapper(client=cognito))
     .register_factory(service=DynamoDbWrapper,
                       factory=lambda: DynamoDbWrapper(tablename=os.environ['DYNAMODB_TABLE'], dynamo_client=dynamo))
     .register(service=ObjectHasher)
     .register(service=IUserGroupsRepo, implementation=DynamoDbUserGroupsRepo)
     .register(service=IGroupRepo, implementation=DynamoDbGroupRepo)
     .register(service=IPropertyRepo, implementation=DynamoDbPropertyRepo)
     .register(service=IRedFlagRepo, implementation=DynamoDbRedFlagRepo))
