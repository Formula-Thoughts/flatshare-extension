from http import HTTPStatus

from formula_thoughts_web.crosscutting import ObjectMapper
from moto import mock_aws

from src.core import IGroupRepo, IUserGroupsRepo, Group
from src.domain.responses import SingleGroupResponse, CreatedGroupResponse, GetGroupCodeResponse, \
    SingleGroupPropertiesResponse
from src.exceptions import GroupNotFoundException
from tests.feature import FeatureTestCase


class LeaveGroupSteps(FeatureTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__object_mapper = self._container.resolve(service=ObjectMapper)
        self.__group_repo = self._container.resolve(service=IGroupRepo)
        self.__user_group_repo = self._container.resolve(service=IUserGroupsRepo)
        self.__group_creator = "user 1"
        self.__group_creator_name = "John Doe"
        self.__group_participant = "user 2"
        self.__group_participant_name = "Jane Doe"

    def a_group_creator_user_exists(self):
        self._cognito.admin_create_user(
            UserPoolId=self._user_pool_id,
            Username=self.__group_creator,
            UserAttributes=[
                {
                    "Name": "name",
                    "Value": self.__group_creator_name
                },
            ]
        )

    def a_participant_user_exists(self):
        self._cognito.admin_create_user(
            UserPoolId=self._user_pool_id,
            Username=self.__group_participant,
            UserAttributes=[
                {
                    "Name": "name",
                    "Value": self.__group_participant_name
                },
            ]
        )

    def a_group_is_created(self):
        create_group_response = self._send_request("POST /groups",
                                                   auth_user_id=self.__group_creator)
        self.__group = self.__object_mapper.map_from_dict(_from=create_group_response.content,
                                                          to=CreatedGroupResponse).group

    def a_participant_is_added(self):
        # arrange
        create_code_response = self._send_request(route_key="GET /groups/{group_id}/code",
                                                  auth_user_id=self.__group_creator,
                                                  path_params={
                                                      "group_id": self.__group.id})
        code = self.__object_mapper.map_from_dict(_from=create_code_response.content,
                                                  to=GetGroupCodeResponse).code
        self._send_request(route_key="POST /participants", auth_user_id=self.__group_participant, params={
            "code": code
        })

        # sense check
        with self.subTest(msg="participant is added to the group"):
            group = self.__group_repo.get(_id=self.__group.id)
            self.assertIn(member=self.__group_participant_name, container=group.participants)

    def a_participant_is_removed(self):
        # act
        self.__response = self._send_request(route_key="DELETE /groups/{group_id}/participants",
                                             auth_user_id=self.__group_participant,
                                             path_params={
                                                 "group_id": self.__group.id
                                             })

    def the_participant_is_removed_from_the_group(self):
        with self.subTest(msg="participant is removed from the group"):
            group = self.__group_repo.get(_id=self.__group.id)
            self.assertNotIn(member=self.__group_participant_name, container=group.participants)

        with self.subTest(msg="group is removed from user groups"):
            user_groups = self.__user_group_repo.get(_id=self.__group_participant)
            self.assertNotIn(member=self.__group.id, container=user_groups.groups)

    def the_response_status_code_is_ok(self):
        with self.subTest(msg="status code is ok"):
            self.assertEqual(self.__response.status, HTTPStatus.OK)

    def the_response_body_contains_group(self):
        with self.subTest(msg="response matches returned group"):
            group = self.__object_mapper.map_from_dict(_from=self._send_request(route_key="GET /groups/{group_id}", auth_user_id=self.__group_participant, path_params={
                "group_id": self.__group.id
            }).content, to=SingleGroupPropertiesResponse)
            group_response = self.__object_mapper.map_from_dict(_from=self.__response.content, to=SingleGroupPropertiesResponse)
            self.assertEqual(group_response, group)


@mock_aws
class TestLeaveGroup(LeaveGroupSteps):

    def setUp(self):
        super().setUp()

    def test_leave_group(self):
        # GIVEN
        self.a_group_creator_user_exists()
        # AND
        self.a_participant_user_exists()
        # AND
        self.a_group_is_created()
        # AND
        self.a_participant_is_added()
        # WHEN
        self.a_participant_is_removed()
        # THEN
        self.the_participant_is_removed_from_the_group()
        # AND
        self.the_response_status_code_is_ok()
        # AND
        self.the_response_body_contains_group()
