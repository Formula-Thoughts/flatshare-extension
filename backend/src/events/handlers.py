from formula_thoughts_web.abstractions import Deserializer
from formula_thoughts_web.application import TopLevelSequenceRunner
from formula_thoughts_web.crosscutting import ObjectMapper
from formula_thoughts_web.events import EventHandlerBase

from src.core import Group, IUpsertGroupBackgroundSequenceBuilder, UserGroups


class UpsertGroupEventHandler(EventHandlerBase):

    def __init__(self, sequence: IUpsertGroupBackgroundSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 object_mapper: ObjectMapper):
        super().__init__(Group,
                         sequence,
                         command_pipeline,
                         deserializer,
                         object_mapper)


class UpsertUserGroupsEventHandler(EventHandlerBase):

    def __init__(self, sequence: IUpsertGroupBackgroundSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 object_mapper: ObjectMapper):
        super().__init__(UserGroups,
                         sequence,
                         command_pipeline,
                         deserializer,
                         object_mapper)