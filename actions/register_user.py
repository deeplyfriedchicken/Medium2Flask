from secrets import EMAIL, PASSWORD

from models.user import UserModel

def registerUser():
    user = UserModel(EMAIL, PASSWORD)
    user.save_to_db()
    return user