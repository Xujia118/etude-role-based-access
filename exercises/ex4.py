from functools import wraps
from data import valid_users  # A dictionary of users


class Authenticator:
    def __init__(self):
        self.users = valid_users
        self.roles = ["admin", "internal_admin",
                      "project_admin", "internal", "external"]
        self.current_user = None

    def _get_role_level(self, role):
        """Return the hierarchy level of a role."""
        return self.roles.index(role) if role in self.roles else len(self.roles)

    def _can_modify_user(self, target_username):
        """Check if current user can modify the target user based on role."""
        if not self.current_user:
            return False  # Must be logged in
        if self.current_user["username"] == target_username:
            return True  # Users can modify their own data

        target_user = self.users.get(target_username)
        if not target_user:
            return False  # Target user doesn't exist

        return self._get_role_level(self.current_user["role"]) <= self._get_role_level(target_user["role"])

    def login(self, username, password):
        """Log in a user."""
        for user in self.users.values():
            if user["username"] == username and user["password"] == password:
                self.current_user = user
                print(f"Logged in as {user['username']}")
                return True
        print("Invalid username or password")
        return False

    def logout(self):
        """Log out the current user."""
        if self.current_user:
            print(f"Logged out {self.current_user['username']}")
            self.current_user = None
        else:
            print("No user is currently logged in")

    def get_current_user(self):
        """Return the currently logged-in user."""
        return self.current_user if self.current_user else None

    def requires_role(self, required_role=None):
        """Decorator to enforce role-based access."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.current_user:
                    print("Access denied! Please log in first.")
                    return None
                if required_role and self._get_role_level(self.current_user["role"]) > self._get_role_level(required_role):
                    print(
                        f"Access denied. Requires {required_role} or higher.")
                    return None
                print(f"Access granted for {self.current_user['username']}")
                return func(*args, **kwargs)
            return wrapper
        return decorator


# Instantiate globally so we can use it for authentication
authenticator = Authenticator()

class UserManager:
    def __init__(self, authenticator):
        self.authenticator = authenticator  # Inject Authenticator dependency
        self.users = self.authenticator.users  # Reference to the same user data

    @authenticator.requires_role("admin")
    def create_user(self, username, password, role):
        """Create a new user with the specified role."""
        if role not in self.authenticator.roles:
            print(f"Invalid role: {role}")
            return False

        current_role_level = self.authenticator._get_role_level(
            self.authenticator.current_user["role"])
        new_role_level = self.authenticator._get_role_level(role)

        if current_role_level > new_role_level:
            print(f"Cannot create user with higher role {role}")
            return False

        if username in self.users:
            print(f"User {username} already exists")
            return False

        self.users[username] = {"username": username,
                                "password": password, "role": role}
        print(f"User {username} created with role {role}")
        return True

    @authenticator.requires_role("admin")
    def delete_user(self, username):
        """Delete a user if the current user has permission."""
        if not self.authenticator._can_modify_user(username):
            print(f"Cannot delete user {username} - insufficient privileges")
            return False

        del self.users[username]
        print(f"User {username} deleted")
        return True

    @authenticator.requires_role("internal_admin")
    def update_user(self, username, password=None, role=None):
        """Update user details such as password and role."""
        if not self.authenticator._can_modify_user(username):
            print(f"Cannot update user {username} - insufficient privileges")
            return False

        if role:
            current_role_level = self.authenticator._get_role_level(
                self.authenticator.current_user["role"])
            new_role_level = self.authenticator._get_role_level(role)

            if current_role_level > new_role_level:
                print(f"Cannot assign higher role {role}")
                return False

            if role not in self.authenticator.roles:
                print(f"Invalid role: {role}")
                return False

            self.users[username]["role"] = role

        if password:
            self.users[username]["password"] = password

        print(f"User {username} updated")
        return True



# Instantiate UserManager and inject authenticator
user_manager = UserManager(authenticator)


# ✅ Login as a regular user
authenticator.login("david", "david")
print(authenticator.get_current_user())  # See logged-in user
user_manager.create_user("john", "password", "internal")  # ❌ Should be denied
authenticator.logout()

# ✅ Login as admin and create a user
authenticator.login("admin", "admin")
user_manager.create_user("john", "password", "internal")  # ✅ Should work
authenticator.logout()

# ✅ Login as John and attempt deletion
authenticator.login("john", "password")
user_manager.delete_user("admin")  # ❌ Should be denied
authenticator.logout()

# ✅ Login as Admin and delete John
authenticator.login("admin", "admin")
user_manager.delete_user("john")  # ✅ Should work
authenticator.logout()
