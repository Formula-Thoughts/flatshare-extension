import typing
import uuid

from formula_thoughts_web.events import SQSEventPublisher, EVENT
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID
from src.domain.errors import invalid_price_error
from src.domain.responses import CreatedGroupResponse


class SetGroupRequestCommand:

    def __init__(self, object_mapper: ObjectMapper):
        self.__object_mapper = object_mapper

    def run(self, context: ApplicationContext) -> None:
        context.set_var(UPSERT_GROUP_REQUEST, self.__object_mapper.map_from_dict(_from=context.body,
                                                                                 to=UpsertGroupRequest))


class ValidateGroupCommand:

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
        group = Group(id=group_id,
                      flats=[],
                      participants=[context.auth_user_id],
                      price_limit=group_request.price_limit,
                      location=group_request.location)
        context.response = CreatedGroupResponse(id=group.id,
                                                flats=group.flats,
                                                participants=group.participants,
                                                price_limit=group.price_limit,
                                                location=group.location)
        context.set_var(GROUP_ID, group_id)
        self.__sqs_event_publisher.send_sqs_message(message_group_id=group_id, payload=group)


class FetchUserGroupsCommand:

    def __init__(self, group_repo: IGroupRepo,
                 user_group_repo: IUserGroupsRepo) -> None:
        self.__user_group_repo = user_group_repo
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext) -> None:
        ...


class CreateUserGroupsAsyncCommand:

    def __init__(self, sqs_event_publisher: SQSEventPublisher) -> None:
        self.__sqs_event_publisher = sqs_event_publisher

    def run(self, context: ApplicationContext) -> None:
        self.__sqs_event_publisher.send_sqs_message(message_group_id=context.auth_user_id,
                                                    payload=UserGroups(auth_user_id=context.auth_user_id,
                                                                       groups=[context.get_var(GROUP_ID, str)]))


class UpsertGroupBackgroundCommand:

    def __init__(self, group_repo: IGroupRepo):
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext) -> None:
        self.__group_repo.create(group=context.get_var(EVENT, Group))


class UpsertUserGroupsBackgroundCommand:

    def __init__(self, user_groups_repo: IUserGroupsRepo):
        self.__user_groups_repo = user_groups_repo

    def run(self, context: ApplicationContext) -> None:
        self.__user_groups_repo.create(user_groups=context.get_var(EVENT, UserGroups))
