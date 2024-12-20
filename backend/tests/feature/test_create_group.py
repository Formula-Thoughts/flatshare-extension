from http import HTTPStatus

from formula_thoughts_web.crosscutting import ObjectMapper
from moto import mock_aws

from src.core import IGroupRepo, IUserGroupsRepo, Group
from src.domain.responses import CreatedGroupResponse
from tests.feature import FeatureTestCase


@mock_aws
class TestCreateGroupSequenceBuilder(FeatureTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__object_mapper = self._container.resolve(service=ObjectMapper)
        self.__group_repo = self._container.resolve(service=IGroupRepo)
        self.__user_group_repo = self._container.resolve(service=IUserGroupsRepo)

    def test_create_group_should_create_group_when_no_groups_exist(self):
        # arrange
        route = "POST /groups"
        auth_user = "test_user"
        self._cognito.admin_create_user(
            UserPoolId=self._user_pool_id,
            Username=auth_user,
            UserAttributes=[
                {
                    "Name": "name",
                    "Value": "John Doe"
                },
            ]
        )

        # act
        response = self._send_request(route_key=route, auth_user_id=auth_user)

        # assert
        with self.subTest(msg="response status is created"):
            self.assertEqual(response.status, HTTPStatus.CREATED)

        # assert
        with self.subTest(msg="group in db matches response"):
            user_groups = self.__user_group_repo.get(_id=auth_user)
            group = self.__group_repo.get(_id=user_groups.groups[0])
            self.assertEqual(self.__object_mapper.map_to_dict(_from=CreatedGroupResponse(group=self.__object_mapper.map(_from=group, to=Group)), to=CreatedGroupResponse),
                             response.content)
