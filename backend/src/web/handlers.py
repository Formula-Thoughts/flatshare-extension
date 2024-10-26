from formula_thoughts_web.abstractions import Deserializer, Logger
from formula_thoughts_web.application import TopLevelSequenceRunner
from formula_thoughts_web.web import ApiRequestHandlerBase

from src.core import IUpdateGroupSequenceBuilder, IFetchUserGroupsSequenceBuilder, ICreatePropertySequenceBuilder, \
    IDeletePropertySequenceBuilder, IAddUserToGroupSequenceBuilder, IGetCodeForGroupSequenceBuilder, \
    IGetUserGroupByIdSequenceBuilder, ICreateGroupSequenceBuilder, ICreateRedFlagSequenceBuilder, \
    IGetRedFlagsSequenceBuilder, ICreateVoteForRedFlagSequenceBuilder, IDeleteVoteForRedFlagSequenceBuilder, \
    IRemoveUserFromGroupSequenceBuilder


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


class CreateGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreateGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /groups',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class CreatePropertyApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreatePropertySequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /groups/{group_id}/properties',
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


class DeletePropertyApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IDeletePropertySequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='DELETE /groups/{group_id}/properties/{property_id}',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class AddCurrentUserToGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IAddUserToGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /participants',
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


class CreateRedFlagApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreateRedFlagSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /red-flags',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class GetRedFlagsApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IGetRedFlagsSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='GET /red-flags',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class CreateVoteForRedFlagApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: ICreateVoteForRedFlagSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='POST /red-flags/{red_flag_id}/votes',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class DeleteVoteForRedFlagApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IDeleteVoteForRedFlagSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='DELETE /red-flags/{red_flag_id}/votes',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)


class RemoveUserFromGroupApiHandler(ApiRequestHandlerBase):

    def __init__(self, sequence: IRemoveUserFromGroupSequenceBuilder,
                 command_pipeline: TopLevelSequenceRunner,
                 deserializer: Deserializer,
                 logger: Logger):
        super().__init__(route_key='DELETE /groups/{group_id}/participants',
                         sequence=sequence,
                         command_pipeline=command_pipeline,
                         deserializer=deserializer,
                         logger=logger)
