from formula_thoughts_web.abstractions import ApiRequestHandler
from formula_thoughts_web.ioc import Container

from src.domain.errors import InvalidGroupDataError, UserGroupsNotFoundError, GroupNotFoundError, PropertyNotFoundError
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse, \
    GetGroupCodeResponse, SingleGroupPropertiesResponse, PropertyCreatedResponse
from src.web.handlers import UpdateGroupApiHandler, FetchUserGroupsApiHandler, CreatePropertyApiHandler, \
    DeletePropertyApiHandler, AddCurrentUserToGroupApiHandler, GetCodeForGroupApiHandler, GetUserGroupByIdApiHandler, \
    CreateGroupApiHandler


def register_web_dependencies(container: Container):
    (container.register(service=ApiRequestHandler, implementation=UpdateGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=CreateGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=FetchUserGroupsApiHandler)
     .register(service=ApiRequestHandler, implementation=CreatePropertyApiHandler)
     .register(service=ApiRequestHandler, implementation=DeletePropertyApiHandler)
     .register(service=ApiRequestHandler, implementation=AddCurrentUserToGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=GetCodeForGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=GetUserGroupByIdApiHandler)
     .register_status_code_mappings(mappings={
         InvalidGroupDataError: 400,
         CreatedGroupResponse: 201,
         ListUserGroupsResponse: 200,
         GetGroupCodeResponse: 200,
         SingleGroupResponse: 200,
         SingleGroupPropertiesResponse: 200,
         PropertyCreatedResponse: 201,
         UserGroupsNotFoundError: 404,
         GroupNotFoundError: 404,
         PropertyNotFoundError: 404
     }))
