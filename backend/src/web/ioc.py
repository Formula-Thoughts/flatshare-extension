from formula_thoughts_web.abstractions import ApiRequestHandler
from formula_thoughts_web.ioc import Container

from src.domain.errors import InvalidGroupError
from src.domain.responses import CreatedGroupResponse
from src.web.handlers import CreateGroupApiHandler


def register_web_dependencies(container: Container):
    (container.register(service=ApiRequestHandler, implementation=CreateGroupApiHandler)
     .register_status_code_mappings(mappings={
         InvalidGroupError: 400,
         CreatedGroupResponse: 201
     }))
