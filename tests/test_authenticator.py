import pytest
from authenticator import Authenticator
from data import valid_users


@pytest.fixture
def authenticator():
    return Authenticator(valid_users.copy())

def test_initial_state(authenticator):
    assert authenticator.current_user is None
    assert authenticator.roles == ["admin", "internal_admin", "project_admin", "internal", "external"]

def test_successful_login(authenticator):
    assert authenticator.login("xujia", "xujia") is True
    assert authenticator.current_user['username'] == 'xujia'
    assert authenticator.current_user['role'] == 'admin'

def test_failed_login(authenticator):
    assert authenticator.login('xujia', 'wrong') is False
    assert authenticator.current_user is None

def test_has_permission_not_logged_in(authenticator):
    for role in authenticator.roles:
        assert authenticator.has_permission(role) is False

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

def test_invalid_role_permission(authenticator):
    authenticator.login('xujia', 'xujia')
    assert authenticator.has_permission('invalid_role') is True