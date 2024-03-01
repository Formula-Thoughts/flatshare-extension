from formula_thoughts_web.abstractions import ApiRequestHandler
from formula_thoughts_web.ioc import Container

from src.domain.errors import InvalidGroupDataError, UserGroupsNotFoundError, GroupNotFoundError
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse
from src.web.handlers import CreateGroupApiHandler, FetchUserGroupsApiHandler, CreateFlatApiHandler


def register_web_dependencies(container: Container):
    (container.register(service=ApiRequestHandler, implementation=CreateGroupApiHandler)
     .register(service=ApiRequestHandler, implementation=FetchUserGroupsApiHandler)
     .register(service=ApiRequestHandler, implementation=CreateFlatApiHandler)
     .register_status_code_mappings(mappings={
         InvalidGroupDataError: 400,
         CreatedGroupResponse: 201,
         ListUserGroupsResponse: 200,
         SingleGroupResponse: 200,
         UserGroupsNotFoundError: 404,
         GroupNotFoundError: 404
     }))
