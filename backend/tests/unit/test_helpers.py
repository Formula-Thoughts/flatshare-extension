from unittest import TestCase

from autofixture import AutoFixture

from src.core import AnonymousRedFlag, RedFlag
from src.domain.helpers import RedFlagMappingHelper
from src.domain.responses import SingleRedFlagResponse


class TestRedFlagMappingHelper(TestCase):

    def setUp(self):
        self.__sut = RedFlagMappingHelper()

    def test_map_to_anonymous_when_user_has_voted(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        red_flag.votes = [user, "12345", "123346"]

        # act
        returned_red_flag = self.__sut.map_to_anonymous(current_user=user, red_flag=red_flag)

        # arrange
        with self.subTest(msg="response is set to red flag"):
            self.assertEqual(returned_red_flag, SingleRedFlagResponse(red_flag=AnonymousRedFlag(
                etag=red_flag.etag,
                partition_key=red_flag.partition_key,
                id=red_flag.id,
                body=red_flag.body,
                property_url=red_flag.property_url,
                votes=3,
                voted_by_me=True,
                date=red_flag.date
            )))

    def test_map_to_anonymous_when_user_has_not_voted(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        red_flag.votes = ["12345", "123346"]

        # act
        returned_red_flag = self.__sut.map_to_anonymous(current_user=user, red_flag=red_flag)

        # arrange
        with self.subTest(msg="response is set to red flag"):
            self.assertEqual(returned_red_flag, SingleRedFlagResponse(red_flag=AnonymousRedFlag(
                etag=red_flag.etag,
                partition_key=red_flag.partition_key,
                id=red_flag.id,
                body=red_flag.body,
                property_url=red_flag.property_url,
                votes=2,
                voted_by_me=False,
                date=red_flag.date
            )))
