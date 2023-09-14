import json
import os
from unittest import TestCase, mock
from unittest.mock import Mock, MagicMock

from server.src.crosscutting import AutoFixture
from server.src.data import S3ClientWrapper
from server.src.data.repositories import GroupRepo
from server.src.domain.models import Group


class BrandRepositoryTestCase(TestCase):

    def setUp(self):
        self.__s3_client: S3ClientWrapper = Mock()
        self.__sut = GroupRepo(self.__s3_client)

    @mock.patch.dict(os.environ, {"S3_BUCKET_NAME": "bucketname"}, clear=True)
    def test_create_group(self):
        # arrange
        data = AutoFixture().create(Group)
        self.__s3_client.put_object = MagicMock()

        # act
        self.__sut.create(data=data)

        # assert
        with self.subTest(msg="s3 object was created once"):
            self.__s3_client.put_object.assert_called_once()

        # assert
        with self.subTest(msg="s3 object was created with correct body"):
            self.__s3_client.put_object.assert_called_with(bucket="bucketname",
                                                           key=f"Group/{data.id}",
                                                           body=json.dumps(data.__dict__, indent=4, sort_keys=True, default=str),
                                                           content_type="application/json")
