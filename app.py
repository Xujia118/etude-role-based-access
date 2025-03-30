from authenticator import Authenticator
from user_mananger import UserManager
from data import valid_users


if __name__ == "__main__":
    auth = Authenticator(valid_users.copy())
    user_manager = UserManager(auth)

    auth.login("xujia", "xujia")
    user_manager.create_user("superman", "superman", "admin")
    user_manager.get_one_user("superman")
    user_manager.get_all_users()
    auth.logout()

