import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from uuid import UUID

from autofixture import AutoFixture
from callee import Any, Captor
from ddt import ddt, data
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper
from formula_thoughts_web.events import SQSEventPublisher

from backend.src.core import UpsertGroupRequest, Group
from backend.src.domain import UPSERT_GROUP_REQUEST
from backend.src.domain.commands import SetGroupRequestContextCommand, ValidateGroupRequestContextCommand, \
    SaveGroupAsyncOverSQSCommand
from backend.src.domain.errors import invalid_price_error


UUID_EXAMPLE = "723f9ec2-fec1-4616-9cf2-576ee632822d"


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
        [price_limit] = price
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=price_limit, location="UK")
        })

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="assert 1 error capsule is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="asser price error capsule is added"):
            self.assertEqual(context.error_capsules[0], invalid_price_error)


class TestSaveGroupAsyncOverSQSCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = SaveGroupAsyncOverSQSCommand(sqs_event_publisher=self.__sqs_event_publisher)


    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    def test_run_should_publish_to_sqs(self, _) -> None:
        # arrange
        group_request = AutoFixture().create(dto=UpsertGroupRequest)
        auth_user_id = "12345"
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: group_request
        },
        auth_user_id=auth_user_id)
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        group_captor = Captor()

        # assert
        with self.subTest(msg="assert sqs message is sent once"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="assert sqs message is sent with correct params"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=UUID_EXAMPLE,
                                                                           payload=Group(
                                                                               id=UUID_EXAMPLE,
                                                                               price_limit=group_request.price_limit,
                                                                               location=group_request.location,
                                                                               flats=[],
                                                                               participants=[auth_user_id]
                                                                           ))