from models.models import UserModel as User

class UserRepository():
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).one_or_none()
        return user
    
    def get_user_by_username(self, username):
        user = self.db.query(User).filter(User.username == username).one_or_none()
        return user

    def get_user_by_email(self, email):
        user = self.db.query(User).filter(User.email == email).one_or_none()
        return user

    def create_user(self, user):
        self.db.add(user)
        self.db.commit()
        return user

    def update_user(self, user):
        self.db.commit()
        return user

    def delete_user(self, user):
        self.db.delete(user)
        self.db.commit()
        return user