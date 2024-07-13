import abc
import os
from typing import TypeVar, Type
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from uuid import UUID

from formula_thoughts_web.abstractions import ApplicationContext, SequenceBuilder
from formula_thoughts_web.application import TopLevelSequenceRunner
from formula_thoughts_web.ioc import Container, register_web

from src.core import IGroupRepo, IUserGroupsRepo, ICreateGroupSequenceBuilder, UserGroups, Group
from src.data import CognitoClientWrapper
from src.domain.ioc import register_domain_dependencies
from src.domain.responses import CreatedGroupResponse
from src.exceptions import UserGroupsNotFoundException
from src.web.ioc import register_web_dependencies

T = TypeVar('T')
UUID_EXAMPLE = "723f9ec2-fec1-4616-9cf2-576ee632822d"
USER_POOL = "test_pool"


class SequenceTestCase(TestCase, abc.ABC):

    def _register(self):
        self._container = Container()
        register_domain_dependencies(container=self._container)
        register_web(services=self._container, default_error_handling_strategy="leave to be determined")
        register_web_dependencies(container=self._container)

    def _run_sequence(self, context: ApplicationContext, type_of_sequence: Type[T]) -> None:
        top_level_sequence = self._container.resolve(type_of_sequence)
        self._container.resolve(TopLevelSequenceRunner).run(context=context, top_level_sequence=top_level_sequence)


class TestCreateGroupSequenceBuilder(SequenceTestCase):

    def setUp(self) -> None:
        self._register()
        self.__group_repo: IGroupRepo = Mock()
        self.__user_groups_repo: IUserGroupsRepo = Mock()
        self.__cognito_client: CognitoClientWrapper = Mock()
        self._container.register_factory(IGroupRepo, lambda: self.__group_repo)
        self._container.register_factory(IUserGroupsRepo, lambda: self.__user_groups_repo)
        self._container.register_factory(CognitoClientWrapper, lambda: self.__cognito_client)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    @patch.dict(os.environ, {"USER_POOL_ID": USER_POOL})
    def test_create_group_should_create_group_when_no_groups_exist(self, _):
        # arrange
        auth_user_id = "test_user1"
        user_name = "Thomas Hardy"
        expected_group = Group(id=UUID_EXAMPLE, participants=[user_name])
        context = ApplicationContext(auth_user_id=auth_user_id,
                                     variables={})
        self.__user_groups_repo.get = MagicMock(side_effect=UserGroupsNotFoundException())
        self.__group_repo.create = MagicMock()
        self.__cognito_client.admin_get_user = MagicMock(return_value={
            'UserAttributes': [
                {
                    'Name': 'name',
                    'Value': user_name
                },
            ]
        })

        # act
        self._run_sequence(context=context, type_of_sequence=ICreateGroupSequenceBuilder)

        # assert
        with self.subTest(msg="assert group is created once"):
            self.__group_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="assert correct group is created once"):
            self.__group_repo.create.assert_called_with(group=expected_group)

        # assert
        with self.subTest(msg="assert correct group is created once"):
            self.assertEqual(context.response, CreatedGroupResponse(group=expected_group))
