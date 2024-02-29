import typing
import uuid

from formula_thoughts_web.events import SQSEventPublisher, EVENT
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID, USER_GROUPS, USER_BELONGS_TO_AT_LEAST_ONE_GROUP
from src.domain.errors import invalid_price_error, UserGroupsNotFoundError
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse
from src.exceptions import UserGroupsNotFoundException


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
        context.response = CreatedGroupResponse(group=group)
        context.set_var(GROUP_ID, group_id)
        self.__sqs_event_publisher.send_sqs_message(message_group_id=group_id, payload=group)


class FetchUserGroupsCommand:

    def __init__(self, group_repo: IGroupRepo,
                 user_group_repo: IUserGroupsRepo) -> None:
        self.__user_group_repo = user_group_repo
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext) -> None:
        try:
            user_groups = self.__user_group_repo.get(_id=context.auth_user_id)
            groups = []
            for group_id in user_groups.groups:
                groups.append(self.__group_repo.get(_id=group_id))
            context.response = ListUserGroupsResponse(groups=groups)
            context.set_var(USER_GROUPS, groups)
        except UserGroupsNotFoundException:
            context.error_capsules.append(UserGroupsNotFoundError(message=f"user group {context.auth_user_id} not found"))


class ValidateIfUserBelongsToAtLeastOneGroupCommand:

    def __init__(self, user_groups_repo: IUserGroupsRepo):
        self.__user_groups_repo = user_groups_repo

    def run(self, context: ApplicationContext) -> None:
        try:
            user_groups = self.__user_groups_repo.get(_id=context.auth_user_id)
            context.set_var(USER_BELONGS_TO_AT_LEAST_ONE_GROUP, True)
            context.set_var(USER_GROUPS, user_groups)
        except UserGroupsNotFoundException:
            context.set_var(USER_BELONGS_TO_AT_LEAST_ONE_GROUP, False)


class CreateUserGroupsAsyncCommand:

    def __init__(self, sqs_event_publisher: SQSEventPublisher) -> None:
        self.__sqs_event_publisher = sqs_event_publisher

    def run(self, context: ApplicationContext) -> None:
        check_if_user_group_exists = context.get_var(name=USER_BELONGS_TO_AT_LEAST_ONE_GROUP, _type=bool)
        user_groups = UserGroups(auth_user_id=context.auth_user_id,
                                 groups=[context.get_var(GROUP_ID, str)])
        if check_if_user_group_exists:
            user_groups.groups =  context.get_var(name=USER_GROUPS, _type=UserGroups).groups + user_groups.groups
        self.__sqs_event_publisher.send_sqs_message(message_group_id=context.auth_user_id,
                                                    payload=user_groups)


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


class ValidateIfGroupBelongsToUser:

    def run(self, context: ApplicationContext) -> None:
        ...