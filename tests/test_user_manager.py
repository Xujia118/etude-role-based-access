import pytest
from authenticator import Authenticator
from user_mananger import UserManager
from data import valid_users


@pytest.fixture
def authenticator():
    return Authenticator(valid_users.copy())


@pytest.fixture
def user_manager(authenticator):
    return UserManager(authenticator)


def test_not_logged_in(user_manager):
    assert user_manager.get_all_users() is None
    assert user_manager.get_one_user('bob') is None
    assert user_manager.get_current_user() is None


def test_get_all_users_admin(user_manager, authenticator):
    authenticator.login('xujia', 'xujia')
    all_users = user_manager.get_all_users()
    print(all_users)
    assert len(all_users) == len(valid_users)


def test_get_one_user(user_manager, authenticator):
    authenticator.login('charlie', 'charlie')
    user = user_manager.get_one_user('bob')
    assert user['username'] == 'bob'
    assert user['role'] == 'project_admin'


def test_get_current_user(user_manager, authenticator):
    authenticator.login('alice', 'alice')
    current_user = user_manager.get_current_user()
    assert current_user['username'] == 'alice'


def test_create_user_admin_success(user_manager, authenticator):
    authenticator.login('xujia', 'xujia')
    assert user_manager.create_user('superman', 'superman', 'admin') is True


def test_create_user_insufficient_roles(user_manager, authenticator):
    authenticator.login('david', 'david')
    assert user_manager.create_user(
        'superman', 'superman', 'project_admin') is False
