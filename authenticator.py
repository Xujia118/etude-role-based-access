class Authenticator:
    """Handles authentication and role verification only"""

    def __init__(self, users_db):
        self.roles = ["admin", "internal_admin", "project_admin", "internal", "external"]
        self.users_db = users_db
        self.current_user = None

    def _get_role_level(self, role):
        """Index 0 is the highest, invalid roles are at the end"""
        try:
            return self.roles.index(role)
        except ValueError:
            return len(self.roles)

    def login(self, username, password):
        """Authenticate a user against the users database"""
        for user in self.users_db.values():
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                print(f"Logged in as {user['username']}")
                return True
        print("Invalid username or password")
        return False

    def logout(self):
        """Clear current session"""
        if self.current_user:
            print(f"Logged out {self.current_user['username']}")
            self.current_user = None
        else:
            print("No user is currently logged in")

    def has_permission(self, target_role):
        """Check if current user has required permissions"""
        if not self.current_user:
            print("Access denied! Please log in first")
            return False

        current_role_level = self._get_role_level(self.current_user['role'])
        target_role_level = self._get_role_level(target_role)

        if current_role_level > target_role_level:
            print(f"Access denied. Requires {self.roles[target_role_level]} or higher")
            return False

        return True

