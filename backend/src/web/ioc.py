from formula_thoughts_web.abstractions import ApiRequestHandler
from formula_thoughts_web.ioc import Container

from src.domain.errors import InvalidGroupError, UserGroupsNotFoundError
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse
from src.web.handlers import CreateGroupApiHandler


def register_web_dependencies(container: Container):
    (container.register(service=ApiRequestHandler, implementation=CreateGroupApiHandler)
     .register_status_code_mappings(mappings={
         InvalidGroupError: 400,
         CreatedGroupResponse: 201,
         ListUserGroupsResponse: 200,
         UserGroupsNotFoundError: 404
     }))
