from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def update_user_city(self, username: str, city: str):
        return self.repository.add_or_update_user(username, city)

    def get_user_city(self, username: str):
        user = self.repository.get_user(username)
        return user.city if user else None