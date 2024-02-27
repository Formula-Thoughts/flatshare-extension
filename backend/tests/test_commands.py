from unittest import TestCase

from ddt import ddt, data
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper

from backend.src.core import UpsertGroupRequest
from backend.src.domain import UPSERT_GROUP_REQUEST
from backend.src.domain.commands import SetGroupRequestContextCommand, ValidateGroupRequestContextCommand
from backend.src.domain.errors import invalid_price_error


class TestSetGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetGroupRequestContextCommand(object_mapper=ObjectMapper())

    def test_run(self):
        # arrange
        location = "UK"
        price_limit = 14.2
        context = ApplicationContext(variables={},
                                     body={"price_limit": price_limit, "location": location})

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="group request is set"):
            create_group_request = context.get_var("UPSERT_GROUP_REQUEST", UpsertGroupRequest)
            self.assertEqual(create_group_request.location, location)
            self.assertEqual(create_group_request.price_limit, price_limit)


@ddt
class TestValidateGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateGroupRequestContextCommand()

    def test_run_with_valid_data(self):
        # arrange
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=14.4, location="UK")
        })

        # act
        self.__sut.run(context)

        # assert
        self.assertEqual(context.error_capsules, [])

    @data([0], [-14])
    def test_run_with_invalid_data(self, price):
        # arrange
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=price, location="UK")
        })

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="assert 1 error capsule is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="asser price error capsule is added"):
            self.assertEqual(context.error_capsules[0], invalid_price_error)
