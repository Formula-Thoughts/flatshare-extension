import os
from dataclasses import dataclass
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

import boto3
from formula_thoughts_web.abstractions import Deserializer, Serializer
from formula_thoughts_web.ioc import Container
from moto import mock_aws

from src.app import bootstrap, run
from src.data import DynamoDbWrapper, CognitoClientWrapper


USER_POOL = "test_pool"


@dataclass
class Response:
    content: dict = None
    status: HTTPStatus = None


class FeatureTestCase(TestCase):

    def setUp(self):
        patch.dict(os.environ, {
            "AWS_ACCESS_KEY_ID": "test",
            "AWS_SECRET_ACCESS_KEY": "test"
        }, clear=True)
        self.__table_name = 'flatini-test'
        self.__default_region = "eu-west-2"
        self._container = Container()
        bootstrap(container=self._container)
        self.__dynamo = boto3.resource('dynamodb', region_name=self.__default_region)
        self._cognito = boto3.client('cognito-idp', region_name=self.__default_region)
        pool = self._cognito.create_user_pool(
            PoolName=USER_POOL,
        )

        cognito_pool_id = pool["UserPool"]["Id"]
        patch.dict(os.environ, {
            "USER_POOL_ID": cognito_pool_id
        }, clear=True)
        self._dynamo_client_wrapper = DynamoDbWrapper(dynamo_client=self.__dynamo,
                                                      tablename=self.__table_name)
        (self._container
         .register_factory(service=DynamoDbWrapper,
                           factory=lambda: self._dynamo_client_wrapper)
         .register_factory(service=CognitoClientWrapper,
                           factory=lambda: CognitoClientWrapper(client=self._cognito)))
        self.__dynamo.create_table(TableName=self.__table_name,
                                   KeySchema=[
                                       {
                                           'AttributeName': 'partition_key',
                                           'KeyType': 'HASH',
                                       },
                                       {
                                           'AttributeName': 'id',
                                           'KeyType': 'RANGE',
                                       }
                                   ],
                                   AttributeDefinitions=[
                                       {
                                           'AttributeName': 'partition_key',
                                           'AttributeType': 'S'
                                       },
                                       {
                                           'AttributeName': 'id',
                                           'AttributeType': 'S'
                                       }
                                   ],
                                   BillingMode='PAY_PER_REQUEST')

    def _send_request(self,
                      route_key: str,
                      auth_user_id: str,
                      path_params: dict = None,
                      params: dict = None,
                      body: dict = None) -> Response:
        event = {'routeKey': route_key}
        if path_params is not None:
            event['pathParameters'] = path_params
        if params is not None:
            event['queryStringParameters'] = params
        if body is not None:
            event['body'] = self._container.resolve(service=Serializer).serialize(data=body)
        response = Response()
        result = run(event=event, context={}, container=self._container)
        if result['body'] is not None:
            response.body = self._container.resolve(service=Deserializer).deserialize(data=result['body'])
        response.status = HTTPStatus(result['statusCode'])
        return response
