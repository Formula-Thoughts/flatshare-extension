from formula_thoughts_web.abstractions import Deserializer
from formula_thoughts_web.application import TopLevelSequenceRunner
from formula_thoughts_web.web import ApiRequestHandlerBase

from backend.src.core import CreateGroupSequenceBuilder


class CreateGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: CreateGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer):
        super().__init__(route_key='POST /groups',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer)
