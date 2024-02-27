from unittest import TestCase

from formula_thoughts_web.abstractions import ApplicationContext

from backend.src.core import UpsertGroupRequest
from backend.src.domain.commands import SetGroupRequestContextCommand


class TestSetGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetGroupRequestContextCommand()

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
