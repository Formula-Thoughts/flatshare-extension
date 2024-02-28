from unittest import TestCase
from unittest.mock import Mock

from src.web.handlers import CreateGroupApiHandler, FetchUserGroupsApiHandler


class TestCreateGroupHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = CreateGroupApiHandler(sequence=Mock(),
                                    command_pipeline=Mock(),
                                    deserializer=Mock())

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
                                        deserializer=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "GET /groups")
