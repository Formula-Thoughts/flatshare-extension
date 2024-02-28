import os
from dataclasses import dataclass
from unittest import TestCase, mock
from unittest.mock import Mock, MagicMock

from autofixture import AutoFixture
from callee import Captor
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeDeserializer, ObjectMapper

from src.core import IBlobRepo, Group, UserGroups
from src.data import S3ClientWrapper
from src.data.repositories import S3BlobRepo, S3GroupRepo, S3UserGroupsRepo


@dataclass(unsafe_hash=True)
class TestDataModel:
    prop_1: int = None
    prop_2: str = None


class BlobRepoTestCase(TestCase):
    def setUp(self):
        self.__s3_wrapper: S3ClientWrapper = Mock()
        self.__serializer = JsonSnakeToCamelSerializer()
        self.__deserializer = JsonCamelToSnakeDeserializer()
        self.__object_mapper = ObjectMapper()
        self.__sut = S3BlobRepo(
            s3_client_wrapper=self.__s3_wrapper,
            serializer=self.__serializer,
            deserializer=self.__deserializer,
            object_mapper=self.__object_mapper
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

    @mock.patch.dict(os.environ, {"S3_BUCKET_NAME": "bucketname"}, clear=True)
    def test_get(self):
        # arrange
        data = AutoFixture().create(TestDataModel)
        self.__s3_wrapper.get_object = MagicMock(return_value=self.__serializer.serialize(data=data.__dict__))

        # act
        response = self.__sut.get(key=f"testmodel/{data.prop_1}/{data.prop_2}", model_type=TestDataModel)

        # assert
        with self.subTest(msg="response matches fetched resource"):
            self.assertEqual(response, data)

        # assert
        with self.subTest(msg="s3 object was created once"):
            self.__s3_wrapper.get_object.assert_called_once()

        # assert
        with self.subTest(msg="s3 object was created with correct body"):
            self.__s3_wrapper.get_object.assert_called_with(
                bucket="bucketname",
                key=f"testmodel/{data.prop_1}/{data.prop_2}",
            )


class TestGroupRepo(TestCase):
    def setUp(self) -> None:
        self.__blob_repo: IBlobRepo = Mock()
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

    def test_get(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        self.__blob_repo.get = MagicMock(return_value=group)

        # act
        response = self.__sut.get(_id=group.id)

        # assert
        with self.subTest(msg="assert blob repo is called once"):
            self.__blob_repo.get.assert_called_once()

        # assert
        with self.subTest(msg="assert blob repo is called with correct args"):
            self.__blob_repo.get.assert_called_with(key=f"groups/{group.id}", model_type=Group)

        with self.subTest(msg="assert response matches group"):
            self.assertEqual(response, group)


class TestUserGroupsRepo(TestCase):

    def setUp(self) -> None:
        self.__blob_repo: IBlobRepo = Mock()
        self.__sut = S3UserGroupsRepo(blob_repo=self.__blob_repo)

    def test_create(self):
        # arrange
        self.__blob_repo.create = MagicMock()
        user_groups = AutoFixture().create(dto=UserGroups)

        # act
        self.__sut.create(user_groups=user_groups)

        # assert
        with self.subTest(msg="assert blob repo is called once"):
            self.__blob_repo.create.assert_called_once()

        # assert
        key_gen_captor = Captor()
        with self.subTest(msg="assert blob repo is called with correct args"):
            self.__blob_repo.create.assert_called_with(
                data=user_groups, key_gen=key_gen_captor
            )

        with self.subTest(msg="assert key gen generates correct key"):
            self.assertEqual(f"user_groups/{user_groups.auth_user_id}", key_gen_captor.arg(user_groups))