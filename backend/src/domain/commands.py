from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper

from backend.src.core import UpsertGroupRequest
from backend.src.domain import UPSERT_GROUP_REQUEST
from backend.src.domain.errors import invalid_price_error


class SetGroupRequestContextCommand:

    def __init__(self, object_mapper: ObjectMapper):
        self.__object_mapper = object_mapper

    def run(self, context: ApplicationContext) -> None:
        context.set_var(UPSERT_GROUP_REQUEST, self.__object_mapper.map_from_dict(_from=context.body,
                                                                                 to=UpsertGroupRequest))


class ValidateGroupRequestContextCommand:

    def run(self, context: ApplicationContext) -> None:
        request = context.get_var(UPSERT_GROUP_REQUEST, UpsertGroupRequest)

        if request.price_limit <= 0:
            context.error_capsules.append(invalid_price_error)
