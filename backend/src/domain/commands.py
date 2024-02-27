import uuid

from formula_thoughts_web.events import SQSEventPublisher
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper

from backend.src.core import UpsertGroupRequest, Group
from backend.src.domain import UPSERT_GROUP_REQUEST
from backend.src.domain.errors import invalid_price_error


class SetGroupRequestCommand:

    def __init__(self, object_mapper: ObjectMapper):
        self.__object_mapper = object_mapper

    def run(self, context: ApplicationContext) -> None:
        context.set_var(UPSERT_GROUP_REQUEST, self.__object_mapper.map_from_dict(_from=context.body,
                                                                                 to=UpsertGroupRequest))


class ValidateGroupRequestCommand:

    def run(self, context: ApplicationContext) -> None:
        request = context.get_var(UPSERT_GROUP_REQUEST, UpsertGroupRequest)

        if request.price_limit <= 0:
            context.error_capsules.append(invalid_price_error)


class CreateGroupAsyncCommand:

    def __init__(self, sqs_event_publisher: SQSEventPublisher) -> None:
        self.__sqs_event_publisher = sqs_event_publisher

    def run(self, context: ApplicationContext) -> None:
        group_request = context.get_var(UPSERT_GROUP_REQUEST, UpsertGroupRequest)
        group_id = str(uuid.uuid4())
        self.__sqs_event_publisher.send_sqs_message(message_group_id=group_id,
                                                    payload=Group(id=group_id,
                                                                  flats=[],
                                                                  participants=[context.auth_user_id],
                                                                  price_limit=group_request.price_limit,
                                                                  location=group_request.location))
