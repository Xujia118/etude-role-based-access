from authenticator import Authenticator
from user_mananger import UserManager
from data import valid_users


if __name__ == "__main__":
    auth = Authenticator(valid_users.copy())
    user_manager = UserManager(auth)

    auth.login("charlie", "charlie")
    user_manager.get_current_user()
    user_manager.create_user("shirley", "shirley", "admin")
    user_manager.get_one_user("david")
    user_manager.update_user("david", "DAVID", "internal_admin")
    auth.logout()

