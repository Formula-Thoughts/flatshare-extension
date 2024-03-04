from formula_thoughts_web.abstractions import Deserializer, Logger
from formula_thoughts_web.application import TopLevelSequenceRunner
from formula_thoughts_web.web import ApiRequestHandlerBase

from src.core import IUpdateGroupSequenceBuilder, IFetchUserGroupsSequenceBuilder, ICreateFlatSequenceBuilder, \
    IDeleteFlatSequenceBuilder, IAddUserToGroupSequenceBuilder, IGetCodeForGroupSequenceBuilder, \
    IGetUserGroupByIdSequenceBuilder


class UpdateGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IUpdateGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='PUT /groups/{group_id}',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class CreateFlatApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreateFlatSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /groups/{group_id}/flats',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class FetchUserGroupsApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IFetchUserGroupsSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='GET /groups',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class DeleteFlatApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IDeleteFlatSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='DELETE /groups/{group_id}/flats/{flat_id}',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class AddCurrentUserToGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IAddUserToGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /participant',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class GetCodeForGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IGetCodeForGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='GET /groups/{group_id}/code',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class GetUserGroupByIdApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IGetUserGroupByIdSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='GET /groups/{group_id}',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)