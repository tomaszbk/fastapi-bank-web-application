from domain.models.models import UserModel as User
from domain.ports.user_repository import UserRepository

class UserSqlAlchemyRepo(UserRepository):

    def __init__(self, db):
        self.db = db

    def get(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).one_or_none()
        return user

    def get_by_username(self, username):
        user = self.db.query(User).filter(User.username == username).one_or_none()
        return user

    def get_by_email(self, email):
        user = self.db.query(User).filter(User.email == email).one_or_none()
        return user

    def create(self, user):
        self.db.add(user)
        self.db.commit()
        return user

    def update(self, user):
        self.db.commit()
        return user

    def delete(self, user):
        self.db.delete(user)
        self.db.commit()
        return user
