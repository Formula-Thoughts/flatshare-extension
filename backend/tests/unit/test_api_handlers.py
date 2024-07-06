from unittest import TestCase
from unittest.mock import Mock

from src.web.handlers import UpdateGroupApiHandler, FetchUserGroupsApiHandler, CreatePropertyApiHandler, \
    DeletePropertyApiHandler, AddCurrentUserToGroupApiHandler, GetCodeForGroupApiHandler, GetUserGroupByIdApiHandler, \
    CreateGroupApiHandler, CreateRedFlagApiHandler, GetRedFlagsApiHandler, CreateVoteForRedFlagApiHandler, \
    DeleteVoteForRedFlagApiHandler


class TestUpdateGroupHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = UpdateGroupApiHandler(sequence=Mock(),
                                    command_pipeline=Mock(),
                                    deserializer=Mock(),
                                    logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "PUT /groups/{group_id}")


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


class TestCreatePropertyApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = CreatePropertyApiHandler(sequence=Mock(),
                                       command_pipeline=Mock(),
                                       deserializer=Mock(),
                                       logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "POST /groups/{group_id}/properties")


class TestDeletePropertyApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = DeletePropertyApiHandler(sequence=Mock(),
                                       command_pipeline=Mock(),
                                       deserializer=Mock(),
                                       logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "DELETE /groups/{group_id}/properties/{property_id}")


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
            self.assertEqual(route_key, "POST /participants")


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


class TestGetUserGroupByIdApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = GetUserGroupByIdApiHandler(sequence=Mock(),
                                         command_pipeline=Mock(),
                                         deserializer=Mock(),
                                         logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "GET /groups/{group_id}")


class TestCreateGroupApiHandler(TestCase):

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


class TestCreateRedFlagApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = CreateRedFlagApiHandler(sequence=Mock(),
                                      command_pipeline=Mock(),
                                      deserializer=Mock(),
                                      logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "POST /red-flags")


class TestGetRedFlagApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = GetRedFlagsApiHandler(sequence=Mock(),
                                    command_pipeline=Mock(),
                                    deserializer=Mock(),
                                    logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "GET /red-flags")


class TestCreateVoteForRedFlagApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = CreateVoteForRedFlagApiHandler(sequence=Mock(),
                                             command_pipeline=Mock(),
                                             deserializer=Mock(),
                                             logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "POST /red-flags/{red_flag_id}/votes")


class TestDeleteVoteForRedFlagApiHandler(TestCase):

    def test_route_key_matches_expected(self):
        # arrange
        sut = DeleteVoteForRedFlagApiHandler(sequence=Mock(),
                                             command_pipeline=Mock(),
                                             deserializer=Mock(),
                                             logger=Mock())

        # act
        route_key = sut.route_key

        # assert
        with self.subTest(msg="route key matches"):
            self.assertEqual(route_key, "DELETE /red-flags/{red_flag_id}/votes")
