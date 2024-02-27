import os
from dataclasses import dataclass
from unittest import TestCase, mock
from unittest.mock import Mock, MagicMock

from autofixture import AutoFixture
from callee import Captor
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeDeserializer

from src.core import IBlobRepo, Group
from src.data import S3ClientWrapper
from src.data.repositories import S3BlobRepo, S3GroupRepo


@dataclass(unsafe_hash=True)
class TestDataModel:
    prop_1: int = None
    prop_2: str = None


class BlobRepoTestCase(TestCase):
    def setUp(self):
        self.__s3_wrapper: S3ClientWrapper = Mock()
        self.__serializer = JsonSnakeToCamelSerializer()
        self.__deserializer = JsonCamelToSnakeDeserializer()
        self.__sut = S3BlobRepo(
            s3_client_wrapper=self.__s3_wrapper,
            serializer=self.__serializer,
            deserializer=self.__deserializer,
        )

    @mock.patch.dict(os.environ, {"S3_BUCKET_NAME": "bucketname"}, clear=True)
    def test_create_group(self):
        # arrange
        data = AutoFixture().create(TestDataModel)
        self.__s3_wrapper.put_object = MagicMock()

        # act
        self.__sut.create(
            data=data, key_gen=lambda x: f"testmodel/{x.prop_1}/{x.prop_2}"
        )

        # assert
        with self.subTest(msg="s3 object was created once"):
            self.__s3_wrapper.put_object.assert_called_once()

        # assert
        with self.subTest(msg="s3 object was created with correct body"):
            self.__s3_wrapper.put_object.assert_called_with(
                bucket="bucketname",
                key=f"testmodel/{data.prop_1}/{data.prop_2}",
                body=self.__serializer.serialize(data=data.__dict__),
                content_type="application/json",
            )


class TestGroupRepo(TestCase):
    def setUp(self) -> None:
        self.__blob_repo: IBlobRepo[Group] = Mock()
        self.__sut = S3GroupRepo(blob_repo=self.__blob_repo)

    def test_create(self):
        # arrange
        self.__blob_repo.create = MagicMock()
        group = AutoFixture().create(dto=Group)

        # act
        self.__sut.create(group=group)

        # assert
        with self.subTest(msg="assert blob repo is called once"):
            self.__blob_repo.create.assert_called_once()

        # assert
        key_gen_captor = Captor()
        with self.subTest(msg="assert blob repo is called with correct args"):
            self.__blob_repo.create.assert_called_with(
                data=group, key_gen=key_gen_captor
            )

        with self.subTest(msg="assert key gen generates correct key"):
            self.assertEqual(f"groups/{group.id}", key_gen_captor.arg(group))
