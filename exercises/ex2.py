from functools import wraps
from data import valid_users


class Authenticate:
    def __init__(self):
        self.users = valid_users
        self.roles = ["admin", "internal_admin",
                      "project_admin", "internal", "external"]
        self.current_user = None

    def _get_role_level(self, role):
        """Index 0 is the highest, invalid roles are at the end"""
        try:
            return self.roles.index(role)
        except ValueError:
            return len(self.roles)

    def _can_modify_user(self, target_username):
        """Check if the user can modify the target user based on their roles"""
        if not self.current_user:
            return False  # Must be logged in

        if self.current_user['username'] == target_username:
            return True  # Users can modify their own data

        target_user = self.users.get(target_username)
        if not target_user:
            return False  # Target user doesn't exist

        current_user_level = self._get_role_level(self.current_user['role'])
        target_user_level = self._get_role_level(target_user['role'])
        return current_user_level <= target_user_level

    def login(self, username, password):
        """Login method"""
        for user in self.users.values():
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                print(f"Logged in as {user['username']}")
                return True
        print("Invalid username or password")
        return False

    def logout(self):
        """Logout method"""
        if self.current_user:
            print(f"Logged out {self.current_user['username']}")
            self.current_user = None
        else:
            print("No user is currently logged in")

    def get_all_users(self):
        if not self.current_user:
            print("No user is currently logged in")
            return None
        
        print(self.users)
        return self.users

    def get_current_user(self):
        if not self.current_user:
            print("No user is currently logged in")
            return None
        
        return self.current_user

    def __call__(self, required_role=None):
        """Decorator implementation"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.current_user:
                    print("Access denied! Please log in first")
                    return None

                if required_role:
                    current_role_level = self._get_role_level(
                        self.current_user['role'])
                    target_role_level = self._get_role_level(required_role)

                    if current_role_level > target_role_level:
                        print(
                            f"Access denied. Requires {required_role} or higher")
                        return None

                print(f"Access granted for {self.current_user['username']}")
                return func(*args, **kwargs)
            return wrapper
        return decorator


# Instantiate auth BEFORE using it as a decorator
auth = Authenticate()


@auth()
def create_user(username, password, role):
    """Create user method"""
    if role not in auth.roles:
        print(f"Invalid role: {role}")
        return False

    current_role_level = auth._get_role_level(auth.current_user['role'])
    new_role_level = auth._get_role_level(role)

    if current_role_level > new_role_level:
        print(f"Cannot create user with higher role {role}")
        return False

    if username in auth.users:
        print(f"User {username} already exists")
        return False

    auth.users[username] = {
        "username": username,
        "password": password,
        "role": role
    }
    print(f"User {username} created with role {role}")
    return True


@auth()
def delete_user(username):
    """Delete user method"""
    if not auth._can_modify_user(username):
        print(f"Cannot delete user {username} - insufficient privileges")
        return False

    del auth.users[username]
    print(f"User {username} deleted")
    return True


@auth()
def update_user(username, password=None, role=None):
    """Update user method"""
    if not auth._can_modify_user(username):
        print(f"Cannot update user {username} - insufficient privileges")
        return False

    if role:
        current_role_level = auth._get_role_level(auth.current_user['role'])
        new_role_level = auth._get_role_level(role)

        if current_role_level > new_role_level:
            print(f"Cannot assign higher role {role}")
            return False

        if role not in auth.roles:
            print(f"Invalid role: {role}")
            return False

        auth.users[username]['role'] = role

    if password:
        auth.users[username]['password'] = password

    print(f"User {username} updated")
    return True


# Test no login
# auth.get_all_users()
# auth.get_current_user()

# Test lowest ranking user
auth.login("david", "david") 
auth.get_all_users()
auth.get_current_user()
# CRUD higher ranking roles, should not be able to
create_user()
auth.logout() 
