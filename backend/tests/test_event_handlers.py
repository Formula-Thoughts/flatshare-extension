from unittest import TestCase
from unittest.mock import Mock

from src.core import Group
from src.events.handlers import UpsertGroupEventHandler


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