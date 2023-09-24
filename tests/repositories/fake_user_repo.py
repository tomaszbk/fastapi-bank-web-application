class FakeUserRepository():
    def __init__(self):
        self.users = []

    def add(self, user):
        self.users.append(user)

    def get(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_by_email(self, email):
        pass

    def update(self, user):
        pass

    def delete(self, user):
        pass
