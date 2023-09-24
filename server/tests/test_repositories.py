import os
from dataclasses import dataclass
from unittest import TestCase, mock
from unittest.mock import Mock, MagicMock

from server.src.core import Serializer, Deserializer
from server.src.crosscutting import AutoFixture
from server.src.data import S3ClientWrapper
from server.src.data.repositories import S3BlobRepo


@dataclass(unsafe_hash=True)
class TestDataModel:
    prop_1: int = None
    prop_2: str = None


class BlobRepoTestCase(TestCase):

    def setUp(self):
        self.__s3_wrapper: S3ClientWrapper = Mock()
        self.__serializer = Serializer()
        self.__deserializer = Deserializer()
        self.__sut = S3BlobRepo(s3_client_wrapper=self.__s3_wrapper,
                                serializer=self.__serializer,
                                deserializer=self.__deserializer)

    @mock.patch.dict(os.environ, {"S3_BUCKET_NAME": "bucketname"}, clear=True)
    def test_create_group(self):
        # arrange
        data = AutoFixture().create(TestDataModel)
        self.__s3_wrapper = MagicMock()

        # act
        self.__sut.create(data=data, key_gen=lambda x: f"testmodel/{x.prop_1}/{x.prop_2}")

        # assert
        with self.subTest(msg="s3 object was created once"):
            self.__s3_wrapper.put_object.assert_called_once()

        # assert
        with self.subTest(msg="s3 object was created with correct body"):
            self.__s3_wrapper.put_object.assert_called_with(bucket="bucketname",
                                                            key=f"testmodel/{data.prop_1}/{data.prop_2}",
                                                            body=self.__serializer.serialize(data=data.__dict__),
                                                            content_type="application/json")
