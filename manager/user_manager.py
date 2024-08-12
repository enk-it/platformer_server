from entities.entities import User


class UserManager:
    def __init__(self):
        self._users = {}

    def add_user(self, user: User) -> None:
        self._users[user.uid] = user

    def remove_user(self, user: User) -> None:
        self._users.pop(user.uid)

    def get_users(self) -> [User]:
        return list(self._users.values())

    def get_user_by_uid(self, uid: str):
        return self._users[uid]