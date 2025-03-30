class UserManager:
    """Handles all CRUD operations for users"""

    def __init__(self, authenticator):
        self.auth = authenticator
        self.users = authenticator.users_db

    def get_all_users(self):
        if not self.auth.has_permission(): # only need to check credentials, so no role passed in
            return None
        
        print("All users:", self.users)
        return self.users
    
    def get_one_user(self, username):
        if not self.auth.has_permission():  # only need to check credentials, so no role passed in
            return None
        
        for user in self.users.values():
            if user['username'] == username:
                print(f"Query result: {user}")
                return user

    def get_current_user(self):
        if not self.auth.has_permission():  # only need to check credentials, so no role passed in
            return None
        
        print("Current user:", self.auth.current_user)
        return self.auth.current_user
    
    def _get_target_user_role(self, target_username):
        # TODO again we need unique identifier
        # but here for simplicity we skip that step

        for user in self.users.values():
            if user['username'] == target_username:
                return user['role']

    def create_user(self, username, password, role):
        if not self.auth.has_permission():  # only need to check credentials, so no role passed in
            return None
        
        # TODO check if the user exists

        if role not in self.auth.roles:
            print(f"Invalid role: {role}")
            return False
        
        if not self.auth.has_permission(role):
            return False
        
        user_id = 1 + len(self.users)

        self.users[str(user_id)] = {
            "username": username,
            "password": password,
            "role": role
        }
        print(f"User {username} created with role {role}")
        return True

    def delete_user(self, username):        
        if not self.auth.has_permission(target_user_role):
            return None
        
        target_user_role = self._get_target_user_role(username);

        if not self.auth.can_modify_user(username, self.users):
            print(f"Cannot delete user {username} - insufficient privileges")
            return False

        del self.users[username]
        print(f"User {username} deleted")
        return True

    def update_user(self, username, password=None, role=None):
        if not self.auth.has_permission(role):
            return None

        for user in self.users.values():
            if user['username'] == username:
                if role:
                    user['role'] = role
                if password:
                    user['password'] = password

        print(f"User {username} updated")
        return True

