import os
import uuid
from unittest import TestCase
from unittest.mock import patch

import boto3
from autofixture import AutoFixture
from botocore.client import BaseClient
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeDeserializer, ObjectMapper
from moto import mock_aws

from src.core import Group, UserGroups
from src.data import S3ClientWrapper
from src.data.repositories import S3GroupRepo, S3BlobRepo, S3UserGroupsRepo
from src.exceptions import GroupNotFoundException, UserGroupsNotFoundException

BUCKET = "test-bucket"


class S3TestCase(TestCase):

    def _set_up_bucket(self):
        self.__s3 = boto3.client('s3')
        self.__s3_client_wrapper = S3ClientWrapper(client=self.__s3)
        self._blob_repo = S3BlobRepo(s3_client_wrapper=self.__s3_client_wrapper,
                                     serializer=JsonSnakeToCamelSerializer(),
                                     deserializer=JsonCamelToSnakeDeserializer(),
                                     object_mapper=ObjectMapper())
        self.__s3.create_bucket(Bucket=BUCKET,
                                CreateBucketConfiguration={
                                    'LocationConstraint': 'eu-west-2',
                                })


class TestGroupRepo(S3TestCase):


    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_by_id(self):
        # arrange
        self._set_up_bucket()
        sut = S3GroupRepo(blob_repo=self._blob_repo)
        stored_group = AutoFixture().create(dto=Group)
        sut.create(group=stored_group)

        # act
        fetched_group = sut.get(_id=stored_group.id)

        # assert
        self.assertEqual(fetched_group, stored_group)

    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_by_id_when_not_found(self):
        # arrange
        self._set_up_bucket()
        sut = S3GroupRepo(blob_repo=self._blob_repo)

        # act/assert
        with self.assertRaises(expected_exception=GroupNotFoundException):
            sut.get(_id=str(uuid.uuid4()))


class TestUserGroupsRepo(S3TestCase):


    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_by_auth_id(self):
        # arrange
        self._set_up_bucket()
        sut = S3UserGroupsRepo(blob_repo=self._blob_repo)
        stored_user_groups = AutoFixture().create(dto=UserGroups)
        sut.create(user_groups=stored_user_groups)

        # act
        fetched_user_groups = sut.get(_id=stored_user_groups.auth_user_id)

        # assert
        self.assertEqual(fetched_user_groups, stored_user_groups)

    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_by_auth_id_when_not_found(self):
        # arrange
        self._set_up_bucket()
        sut = S3UserGroupsRepo(blob_repo=self._blob_repo)

        # act/assert
        with self.assertRaises(expected_exception=UserGroupsNotFoundException):
            sut.get(_id=str(uuid.uuid4()))