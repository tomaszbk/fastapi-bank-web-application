from bank_of_kukelia.domain.models import User

def user_already_exists(username: str, repo =UserRepository()):
    return repo.get_user(username) is not None


def create_user(username: str, password: str):
    return User(username=username, password=password)