import os
from unittest import TestCase
from unittest.mock import patch

import boto3
from formula_thoughts_web.crosscutting import ObjectMapper, JsonSnakeToCamelSerializer
from moto import mock_aws

from src.data import ObjectHasher, DynamoDbWrapper


@patch.dict(os.environ, {
    "AWS_ACCESS_KEY_ID": "test",
    "AWS_SECRET_ACCESS_KEY": "test"
}, clear=True)
class DynamoDbTestCase(TestCase):

    def setUp(self):
        self._object_mapper = ObjectMapper()
        self._object_hasher = ObjectHasher(object_mapper=self._object_mapper, serializer=JsonSnakeToCamelSerializer())
        table_name = 'flatini-test'
        self.__dynamo = boto3.resource('dynamodb', region_name="eu-west-2")
        self._dynamo_client_wrapper = DynamoDbWrapper(dynamo_client=self.__dynamo, tablename=table_name)
        self.__dynamo.create_table(TableName=table_name,
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
