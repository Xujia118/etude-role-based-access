import pytest
from authenticator import Authenticator
from data import valid_users


@pytest.fixture
def authenticator():
    return Authenticator(valid_users.copy())


def test_initial_state(authenticator):
    assert authenticator.current_user is None
    assert authenticator.roles == [
        "admin", "internal_admin", "project_admin", "internal", "external"]


def test_successful_login(authenticator):
    assert authenticator.login("xujia", "xujia") is True
    assert authenticator.current_user['username'] == 'xujia'
    assert authenticator.current_user['role'] == 'admin'


def test_failed_login(authenticator):
    assert authenticator.login('xujia', 'wrong') is False
    assert authenticator.current_user is None


def test_logout_with_user(authenticator):
    authenticator.login("xujia", "xujia")
    authenticator.logout()
    assert authenticator.current_user is None


def test_logout_no_user(authenticator):
    authenticator.logout()  # Should print "No user is currently logged in"
    assert authenticator.current_user is None


def test_get_role_level(authenticator):
    assert authenticator._get_role_level('admin') == 0
    assert authenticator._get_role_level('non_existing_role') == 5


# not logged in, so no role
def test_has_permission_not_logged_in(authenticator):
    assert authenticator.has_permission('admin') is False 

# logged in, but wrong role
def test_invalid_role_permission(authenticator):
    authenticator.login('xujia', 'xujia')
    assert authenticator.has_permission('invalid_role') is False


def test_external_user_permission_denied(authenticator):
    authenticator.login("eve", "eve")  # Assuming 'eve' is 'external'
    assert authenticator.has_permission("internal") is False  # Should fail


def test_has_permission_admin(authenticator):
    authenticator.login('xujia', 'xujia')
    assert authenticator.has_permission('admin')
    assert authenticator.has_permission('internal_admin')
    assert authenticator.has_permission('project_admin')
    assert authenticator.has_permission('internal')
    assert authenticator.has_permission('external')


def test_has_permission_internal_admin(authenticator):
    authenticator.login('alice', 'alice')
    assert authenticator.has_permission('admin') is False
    assert authenticator.has_permission('internal_admin')
    assert authenticator.has_permission('project_admin')
    assert authenticator.has_permission('internal')
    assert authenticator.has_permission('external')
