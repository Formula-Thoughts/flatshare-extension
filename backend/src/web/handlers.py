from formula_thoughts_web.abstractions import Deserializer
from formula_thoughts_web.application import TopLevelSequenceRunner
from formula_thoughts_web.web import ApiRequestHandlerBase

from src.core import ICreateGroupSequenceBuilder, IFetchUserGroupsSequenceBuilder, ICreateFlatSequenceBuilder


class CreateGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreateGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer):
        super().__init__(route_key='POST /groups',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer)


class CreateFlatApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreateFlatSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer):
        super().__init__(route_key='POST /groups/{group_id}/flats',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer)


class FetchUserGroupsApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IFetchUserGroupsSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer):
        super().__init__(route_key='GET /groups',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer)