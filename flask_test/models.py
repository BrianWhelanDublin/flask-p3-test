from flask_test import mongo, login_manager


class User:
    def __init__(self, user):
        
        self.username = user["username"]
        self.email = user["email"]
        self.posts = user["posts"]

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_posts(self):
        return self.posts


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return None
    return User(user)
