from unittest import TestCase
from unittest.mock import Mock

from src.core import Group, UserGroups
from src.events.handlers import UpsertGroupEventHandler, UpsertUserGroupsEventHandler


class TestUpsertGroupEventHandler(TestCase):

    def setUp(self):
        self.__sut = UpsertGroupEventHandler(sequence=Mock(),
                                             command_pipeline=Mock(),
                                             deserializer=Mock(),
                                             object_mapper=Mock())

    def test_event_should_be_group(self):
        # act
        event = self.__sut.event_type

        # assert
        self.assertEqual(event, Group)


class TestUpsertUserGroupsEventHandler(TestCase):

    def setUp(self):
        self.__sut = UpsertUserGroupsEventHandler(sequence=Mock(),
                                                  command_pipeline=Mock(),
                                                  deserializer=Mock(),
                                                  object_mapper=Mock())

    def test_event_should_be_user_groups(self):
        # act
        event = self.__sut.event_type

        # assert
        self.assertEqual(event, UserGroups)
