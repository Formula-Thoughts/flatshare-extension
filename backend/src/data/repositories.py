from boto3.dynamodb.conditions import Attr, Key, ConditionExpressionBuilder, Or
from botocore.exceptions import ClientError
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import Group, UserGroups, Property, GroupParticipantName, GroupId, GroupProperties, PropertyId
from src.data import DynamoDbWrapper, ObjectHasher, CONDITIONAL_CHECK_FAILED
from src.exceptions import UserGroupsNotFoundException, GroupNotFoundException, ConflictException, \
    GroupAlreadyExistsException, UserGroupAlreadyExistsException, PropertyNotFoundException


class DynamoDbPropertyRepo:

    def __init__(self, dynamo_wrapper: DynamoDbWrapper,
                 object_mapper: ObjectMapper,
                 object_hasher: ObjectHasher):
        self.__object_hasher = object_hasher
        self.__object_mapper = object_mapper
        self.__dynamo_wrapper = dynamo_wrapper

    def create(self, group_id: GroupId, property: Property) -> None:
        self.__partition_key_gen(property, group_id)
        self.__id_setter(property)
        property.etag = self.__object_hasher.hash(object=property)
        prop_dict = self.__object_mapper.map_to_dict(_from=property, to=Property, preserve_decimal=True)
        self.__dynamo_wrapper.put(item=prop_dict,
                                  condition_expression=Attr('etag').not_exists())
        property.id = property.id.split(":")[1]

    def delete(self, group_id: GroupId, property_id: PropertyId) -> None:
        try:
            self.__dynamo_wrapper.delete_item(key={
                "id": f"property:{property_id}",
                "partition_key": f"group:{group_id}"
            }, condition_expression=Attr('etag').exists())
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == CONDITIONAL_CHECK_FAILED:
                raise PropertyNotFoundException()

    @staticmethod
    def __partition_key_gen(property: Property, group: GroupId) -> None:
        property.partition_key = f"group:{group}"

    @staticmethod
    def __id_setter(property: Property):
        property.id = f"property:{property.id}"


class DynamoDbGroupRepo:

    def __init__(self, dynamo_wrapper: DynamoDbWrapper,
                 object_mapper: ObjectMapper,
                 object_hasher: ObjectHasher):
        self.__object_hasher = object_hasher
        self.__object_mapper = object_mapper
        self.__dynamo_wrapper = dynamo_wrapper

    def create(self, group: Group) -> None:
        try:
            group_id = group.id
            self.__partition_key_gen(group, group_id)
            self.__id_setter(group, group_id)
            group.etag = self.__object_hasher.hash(object=group)
            group_dict = self.__object_mapper.map_to_dict(_from=group, to=Group, preserve_decimal=True)
            self.__dynamo_wrapper.put(item=group_dict,
                                      condition_expression=Attr('etag').not_exists())
            group.id = group_id
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == CONDITIONAL_CHECK_FAILED:
                raise GroupAlreadyExistsException()

    def update(self, group: Group) -> None:
        try:
            group_id = group.id
            prev_etag = group.etag
            self.__id_setter(group=group, group_id=group_id)
            group.etag = self.__object_hasher.hash(object=group)
            self.__dynamo_wrapper.put(item=self.__object_mapper.map_to_dict(_from=group, to=Group, preserve_decimal=True),
                                      condition_expression=Attr('etag').eq(prev_etag))
            group.id = group_id
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == CONDITIONAL_CHECK_FAILED:
                raise ConflictException()

    def get(self, _id: str) -> GroupProperties:
        items = self.__dynamo_wrapper.query(key_condition_expression="partition_key = :partition_key",
                                            expression_attribute_values={
                                                ":partition_key": f"group:{_id}",
                                            })["Items"]
        if len(items) == 0:
            raise GroupNotFoundException(f"Group with id {_id} not found")
        property_dicts = []
        properties = []
        group = None
        for item in items:
            if 'property' in item['id']:
                property_dicts.append(item)
            else:
                group = item
        group = self.__object_mapper.map_from_dict(_from=group, to=Group)
        for property_dict in property_dicts:
            prop = self.__object_mapper.map_from_dict(_from=property_dict, to=Property)
            prop.id = prop.id.split(":")[1]
            properties.append(prop)

        return GroupProperties(etag=group.etag,
                               partition_key=group.partition_key,
                               id=_id,
                               participants=group.participants,
                               price_limit=group.price_limit,
                               locations=group.locations,
                               properties=properties)

    def add_participant(self, participant: GroupParticipantName, group: Group) -> None:
        try:
            group.participants.append(participant)
            new_hash = self.__object_hasher.hash(object=group)
            self.__dynamo_wrapper.update_item(key={
                "id": f"group:{group.id}",
                "partition_key": f"group:{group.id}"
            },
                update_expression="SET participants = list_append(participants, :i) SET etag = :j",
                condition_expression=Attr("etag").eq(group.etag),
                expression_attribute_values={
                    ':i': [participant],
                    ':j': new_hash
                })
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == CONDITIONAL_CHECK_FAILED:
                raise ConflictException()

    @staticmethod
    def __partition_key_gen(group: Group, group_id):
        group.partition_key = f"group:{group_id}"

    @staticmethod
    def __id_setter(group: Group, group_id):
        group.id = f"group:{group_id}"


class DynamoDbUserGroupsRepo:

    def __init__(self, dynamo_wrapper: DynamoDbWrapper,
                 object_mapper: ObjectMapper,
                 object_hasher: ObjectHasher):
        self.__object_hasher = object_hasher
        self.__object_mapper = object_mapper
        self.__dynamo_wrapper = dynamo_wrapper

    def get(self, _id: str) -> UserGroups:
        items = self.__dynamo_wrapper.query(key_condition_expression="id = :id and partition_key = :partition_key",
                                            expression_attribute_values={
                                                ':id': _id,
                                                ':partition_key': f"user_group:{_id}"
                                            })["Items"]
        if len(items) == 0:
            raise UserGroupsNotFoundException()
        user_groups = items[0]
        return self.__object_mapper.map_from_dict(_from=user_groups, to=UserGroups)

    def create(self, user_groups: UserGroups) -> None:
        try:
            self.__partition_key_gen(user_groups=user_groups)
            user_groups.etag = self.__object_hasher.hash(object=user_groups)
            item = self.__object_mapper.map_to_dict(_from=user_groups, to=UserGroups)
            self.__dynamo_wrapper.put(item=item,
                                      condition_expression=Attr('etag').not_exists())
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == CONDITIONAL_CHECK_FAILED:
                raise UserGroupAlreadyExistsException()

    def add_group(self, user_groups: UserGroups, group: GroupId) -> None:
        try:
            user_groups.groups.append(group)
            new_hash = self.__object_hasher.hash(object=user_groups)
            self.__dynamo_wrapper.update_item(key={
                "id": user_groups.id,
                "partition_key": f"user_group:{user_groups.id}"
            },
                update_expression="SET groups = list_append(groups, :i) SET etag = :j",
                condition_expression=Attr("etag").eq(user_groups.etag),
                expression_attribute_values={
                    ':i': [group],
                    ':j': new_hash
                })
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == CONDITIONAL_CHECK_FAILED:
                raise ConflictException()


    @staticmethod
    def __partition_key_gen(user_groups: UserGroups):
        user_groups.partition_key = f"user_group:{user_groups.id}"
