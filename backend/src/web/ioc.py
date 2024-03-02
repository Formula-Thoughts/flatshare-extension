from formula_thoughts_web.abstractions import ApiRequestHandler
from formula_thoughts_web.ioc import Container

from src.domain.errors import InvalidGroupDataError, UserGroupsNotFoundError, GroupNotFoundError, FlatNotFoundError
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse, GetGroupCodeResponse
from src.web.handlers import CreateGroupApiHandler, FetchUserGroupsApiHandler, CreateFlatApiHandler, \
    DeleteFlatApiHandler, AddCurrentUserToGroupApiHandler, GetCodeForGroupApiHandler


def register_web_dependencies(container: Container):
    (container.register(service=ApiRequestHandler, implementation=CreateGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=FetchUserGroupsApiHandler)
     .register(service=ApiRequestHandler, implementation=CreateFlatApiHandler)
     .register(service=ApiRequestHandler, implementation=DeleteFlatApiHandler)
     .register(service=ApiRequestHandler, implementation=AddCurrentUserToGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=GetCodeForGroupApiHandler)
     .register_status_code_mappings(mappings={
         InvalidGroupDataError: 400,
         CreatedGroupResponse: 201,
         ListUserGroupsResponse: 200,
         GetGroupCodeResponse: 200,
         SingleGroupResponse: 200,
         UserGroupsNotFoundError: 404,
         GroupNotFoundError: 404,
         FlatNotFoundError: 404
     }))
