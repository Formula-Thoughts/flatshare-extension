import base64
import datetime
import os
import uuid

import formula_thoughts_web.crosscutting
from formula_thoughts_web.abstractions import ApplicationContext, Logger
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups, CreatePropertyRequest, \
    Property, GroupProperties, IPropertyRepo, IRedFlagRepo, RedFlag, CreateRedFlagRequest
from src.data import CognitoClientWrapper
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID, USER_GROUPS, USER_BELONGS_TO_AT_LEAST_ONE_GROUP, GROUP, \
    CREATE_PROPERTY_REQUEST, PROPERTY_ID, CODE, FULLNAME_CLAIM, RED_FLAG, CREATE_RED_FLAG_REQUEST
from src.domain.errors import invalid_price_error, UserGroupsNotFoundError, GroupNotFoundError, \
    PropertyNotFoundError, \
    code_required_error, user_already_part_of_group_error, \
    property_price_required_error, property_url_required_error, property_title_required_error, \
    red_flag_body_required_error, red_flag_property_url_required_error
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse, \
    GetGroupCodeResponse, SingleGroupPropertiesResponse, PropertyCreatedResponse
from src.exceptions import UserGroupsNotFoundException, GroupNotFoundException, PropertyNotFoundException


class SetGroupRequestCommand:

    def __init__(self, object_mapper: ObjectMapper,
                 logger: Logger):
        self.__logger = logger
        self.__object_mapper = object_mapper

    def run(self, context: ApplicationContext) -> None:
        group_request = self.__object_mapper.map_from_dict(_from=context.body,
                                                           to=UpsertGroupRequest)
        context.set_var(UPSERT_GROUP_REQUEST, self.__object_mapper.map_from_dict(_from=context.body,
                                                                                 to=UpsertGroupRequest))
        self.__logger.add_global_properties(properties={
            'locations': group_request.locations,
            'price_limit': group_request.price_limit
        })


class ValidateGroupCommand:

    def run(self, context: ApplicationContext) -> None:
        request = context.get_var(UPSERT_GROUP_REQUEST, UpsertGroupRequest)

        if request.price_limit is None:
            return

        if request.price_limit <= 0:
            context.error_capsules.append(invalid_price_error)


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
            context.response = ListUserGroupsResponse(group_properties_list=groups)
            context.set_var(USER_GROUPS, groups)
        except UserGroupsNotFoundException:
            context.error_capsules.append(
                UserGroupsNotFoundError(message=f"user group {context.auth_user_id} not found"))


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


class ValidateIfGroupBelongsToUserCommand:

    def run(self, context: ApplicationContext) -> None:
        if not context.get_var(name=USER_BELONGS_TO_AT_LEAST_ONE_GROUP, _type=bool):
            context.error_capsules.append(UserGroupsNotFoundError(message=f"current user has no groups"))
            return
        user_groups = context.get_var(name=USER_GROUPS, _type=UserGroups)
        group_id_from_request = context.get_var(name=GROUP_ID, _type=str)
        if not any(group_id_from_request in group_id for group_id in user_groups.groups):
            context.error_capsules.append(GroupNotFoundError(message=f"group {group_id_from_request} not found for "
                                                                     f"current user"))


class FetchGroupByIdCommand:

    def __init__(self, group_repo: IGroupRepo):
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext):
        group_id = context.get_var(name=GROUP_ID, _type=str)
        try:
            group = self.__group_repo.get(_id=group_id)
            context.set_var(GROUP, group)
            context.response = SingleGroupPropertiesResponse(group_properties=group)
        except GroupNotFoundException:
            context.error_capsules.append(GroupNotFoundError(message=f"group {group_id} not found"))


class SetPropertyRequestCommand:

    def __init__(self, object_mapper: ObjectMapper,
                 logger: Logger):
        self.__logger = logger
        self.__object_mapper = object_mapper

    def run(self, context: ApplicationContext):
        request = self.__object_mapper.map_from_dict(_from=context.body, to=CreatePropertyRequest)
        context.set_var(CREATE_PROPERTY_REQUEST, request)
        self.__logger.add_global_properties(properties={
            "location": request.title,
            "price": request.price,
            "url": request.url
        })


class CreatePropertyCommand:

    def __init__(self, property_repo: IPropertyRepo):
        self.__property_repo = property_repo

    def run(self, context: ApplicationContext):
        group = context.get_var(name=GROUP, _type=Group)
        user_groups = context.get_var(name=USER_GROUPS, _type=UserGroups)
        property_request = context.get_var(name=CREATE_PROPERTY_REQUEST, _type=CreatePropertyRequest)
        property = Property(url=property_request.url,
                            title=property_request.title,
                            price=property_request.price,
                            full_name=user_groups.name)
        self.__property_repo.create(group_id=group.id, property=property)
        context.response = PropertyCreatedResponse(property=property)


class ValidatePropertyRequestCommand:

    def run(self, context: ApplicationContext):
        create_property_request = context.get_var(name=CREATE_PROPERTY_REQUEST, _type=CreatePropertyRequest)

        if create_property_request.price is None:
            context.error_capsules.append(property_price_required_error)
        elif create_property_request.price <= 0:
            context.error_capsules.append(invalid_price_error)

        if create_property_request.url is None:
            context.error_capsules.append(property_url_required_error)

        if create_property_request.title is None:
            context.error_capsules.append(property_title_required_error)


class DeletePropertyCommand:

    def __init__(self, property_repo: IPropertyRepo):
        self.__property_repo = property_repo

    def run(self, context: ApplicationContext):
        try:
            property_id = context.get_var(name=PROPERTY_ID, _type=str)
            group = context.get_var(name=GROUP, _type=Group)
            self.__property_repo.delete(group_id=group.id, property_id=property_id)
            context.response = None
        except PropertyNotFoundException:
            context.error_capsules.append(PropertyNotFoundError())


class AddCurrentUserToGroupCommand:

    def __init__(self, group_repo: IGroupRepo):
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext):
        fullname = context.get_var(name=FULLNAME_CLAIM, _type=str)
        group_properties = context.get_var(name=GROUP, _type=GroupProperties)
        group = Group(etag=group_properties.etag,
                      partition_key=group_properties.partition_key,
                      id=group_properties.id,
                      participants=group_properties.participants,
                      price_limit=group_properties.price_limit,
                      locations=group_properties.locations)
        self.__group_repo.add_participant(participant=fullname, group=group)
        context.response = SingleGroupResponse(group=group)


class SetGroupIdFromCodeCommand:

    def run(self, context: ApplicationContext):
        try:
            code = context.get_var(name=CODE, _type=str)
            group_id = base64.b64decode(code).decode('utf-8')
            context.set_var(name=GROUP_ID, value=str(group_id))
        except KeyError:
            context.error_capsules.append(code_required_error)


class GetCodeFromGroupIdCommand:

    def run(self, context: ApplicationContext):
        group_id = context.get_var(name=GROUP_ID, _type=str)
        code = base64.b64encode(group_id.encode('utf-8')).decode('utf-8')
        context.response = GetGroupCodeResponse(code=code)


class ValidateUserIsNotParticipantCommand:

    def run(self, context: ApplicationContext):
        group = context.get_var(name=GROUP, _type=Group)
        fullname = context.get_var(name=FULLNAME_CLAIM, _type=str)
        if fullname in group.participants:
            context.error_capsules.append(user_already_part_of_group_error)
            return


class CreateGroupCommand:

    def __init__(self, group_repo: IGroupRepo):
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext):
        group_id = str(uuid.uuid4())
        fullname = context.get_var(name=FULLNAME_CLAIM, _type=str)
        group = Group(id=group_id,
                      participants=[fullname])
        self.__group_repo.create(group=group)
        context.response = CreatedGroupResponse(group=group)
        context.set_var(name=GROUP_ID, value=group_id)


class FetchAuthUserClaimsIfUserDoesNotExistCommand:

    def __init__(self, cognito_wrapper: CognitoClientWrapper):
        self.__cognito_wrapper = cognito_wrapper

    def run(self, context: ApplicationContext):
        is_user_part_of_at_least_one_group = context.get_var(name=USER_BELONGS_TO_AT_LEAST_ONE_GROUP, _type=str)
        if is_user_part_of_at_least_one_group:
            context.set_var(name=FULLNAME_CLAIM,
                            value=context.get_var(name=USER_GROUPS, _type=UserGroups).name)
            return

        user = self.__cognito_wrapper.admin_get_user(user_pool_id=os.environ["USER_POOL_ID"],
                                                     username=context.auth_user_id)

        context.set_var(name=FULLNAME_CLAIM,
                        value=list(filter(lambda x: x['Name'] == "name", user['UserAttributes']))[0]['Value'])


class CreateUserGroupsCommand:

    def __init__(self, user_groups_repo: IUserGroupsRepo) -> None:
        self.__user_groups_repo = user_groups_repo

    def run(self, context: ApplicationContext) -> None:
        user_group_exists = context.get_var(name=USER_BELONGS_TO_AT_LEAST_ONE_GROUP, _type=bool)
        user_group_id = context.get_var(GROUP_ID, str)
        if user_group_exists:
            current_user_groups = context.get_var(name=USER_GROUPS, _type=UserGroups)
            self.__user_groups_repo.add_group(user_groups=current_user_groups, group=user_group_id)
        else:
            user_groups = UserGroups(id=context.auth_user_id,
                                     groups=[user_group_id])
            user_groups.name = context.get_var(name=FULLNAME_CLAIM, _type=str)
            self.__user_groups_repo.create(user_groups=user_groups)
            context.set_var(name=USER_GROUPS, value=user_groups)


class UpdateGroupCommand:

    def __init__(self, group_repo: IGroupRepo) -> None:
        self.__group_repo = group_repo

    def run(self, context: ApplicationContext) -> None:
        group_request = context.get_var(UPSERT_GROUP_REQUEST, UpsertGroupRequest)
        group_from_store = context.get_var(GROUP, GroupProperties)
        group_to_update = Group(id=group_from_store.id,
                                etag=group_from_store.etag,
                                partition_key=group_from_store.partition_key,
                                participants=group_from_store.participants,
                                price_limit=group_request.price_limit,
                                locations=group_request.locations)
        self.__group_repo.update(group=group_to_update)
        context.response = SingleGroupResponse(group=group_to_update)


class CreateRedFlagCommand:

    def __init__(self, red_flag_repo: IRedFlagRepo):
        self.__red_flag_repo = red_flag_repo

    def run(self, context: ApplicationContext) -> None:
        red_flag_request = context.get_var(name=CREATE_RED_FLAG_REQUEST,
                                           _type=CreateRedFlagRequest)
        red_flag = RedFlag(body=red_flag_request.body,
                           property_url=red_flag_request.property_url,
                           date=formula_thoughts_web.crosscutting.utc_now())
        self.__red_flag_repo.create(red_flag=red_flag)
        context.set_var(name=RED_FLAG,
                        value=red_flag)


class SetRedFlagRequestCommand:

    def __init__(self, object_mapper: ObjectMapper):
        self.__object_mapper = object_mapper

    def run(self, context: ApplicationContext) -> None:
        create_red_flag_request = self.__object_mapper.map_from_dict(_from=context.body,
                                                                     to=CreateRedFlagRequest)
        context.set_var(name=CREATE_RED_FLAG_REQUEST, value=create_red_flag_request)


class ValidateRedFlagRequestCommand:

    def run(self, context: ApplicationContext) -> None:
        red_flag_request = context.get_var(name=CREATE_RED_FLAG_REQUEST, _type=CreateRedFlagRequest)

        if red_flag_request.body is None:
            context.error_capsules.append(red_flag_body_required_error)

        if red_flag_request.property_url is None:
            context.error_capsules.append(red_flag_property_url_required_error)


class SetAnonymousRedFlagCommand:

    def run(self, context: ApplicationContext) -> None:
        ...