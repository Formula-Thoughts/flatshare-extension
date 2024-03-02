from unittest import TestCase
from unittest.mock import Mock

from src.web.handlers import CreateGroupApiHandler, FetchUserGroupsApiHandler, CreateFlatApiHandler, \
    DeleteFlatApiHandler, AddCurrentUserToGroupApiHandler, GetCodeForGroupApiHandler


class TestCreateGroupHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = CreateGroupApiHandler(sequence=Mock(),
                                    command_pipeline=Mock(),
                                    deserializer=Mock(),
                                    logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "POST /groups")


class TestFetchUserGroupsApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = FetchUserGroupsApiHandler(sequence=Mock(),
                                        command_pipeline=Mock(),
                                        deserializer=Mock(),
                                        logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "GET /groups")


class TestCreateFlatApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = CreateFlatApiHandler(sequence=Mock(),
                                   command_pipeline=Mock(),
                                   deserializer=Mock(),
                                   logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "POST /groups/{group_id}/flats")


class TestDeleteFlatApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = DeleteFlatApiHandler(sequence=Mock(),
                                   command_pipeline=Mock(),
                                   deserializer=Mock(),
                                   logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "DELETE /groups/{group_id}/flats/{flat_id}")


class TestAddCurrentUserToGroupApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = AddCurrentUserToGroupApiHandler(sequence=Mock(),
                                              command_pipeline=Mock(),
                                              deserializer=Mock(),
                                              logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "POST /participant")


class TestGetCodeForGroupApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = GetCodeForGroupApiHandler(sequence=Mock(),
                                        command_pipeline=Mock(),
                                        deserializer=Mock(),
                                        logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "GET /groups/{group_id}/code")
