class Authenticator:
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        valid_users = {
            'admin': "secret123",
            "user": "password123"
        }

        if username not in valid_users:
            print(f"User '{username}' does not exist")
            return

        if password != valid_users[username]:
            print(f"Incorrect password")
            return

        self.current_user = {
            "username": username,
            "role": "admin" if username == "admin" else "user"
        }

        print(f"Welcome, {username}")
        return

    def logout(self):
        self.current_user = None

    def __call__(self, required_role=None):
        """Decorator implementation"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.current_user:
                    print("Access denied! Please log in first")
                    return

                if required_role is not None and self.current_user['role'] != required_role:
                    print(f"Access denied. Requires {required_role}.")
                    return

                print(f"Access granted for {self.current_user['username']}")
                return func(*args, **kwargs)
            return wrapper
        return decorator


auth = Authenticator()


@auth(required_role="admin")
def delete_database():
    print("Database deleted!")


@auth()
def view_profile():
    print("Displaying your profile")


# auth.login("teacher", "teacher")
# auth.login("admin", "admin")

auth.login("admin", "secret123")
view_profile()
delete_database()
auth.logout()

auth.login("user", "password123")
view_profile()
delete_database()
auth.logout()

