from werkzeug.security import check_password_hash, generate_password_hash       
from flask_login import UserMixin


class User(UserMixin):
    
    def __init__(self, id, namee, email, password_hash):
        self.id = id
        self.namee = namee
        self.email = email  
        self.password_hash = password_hash


    @classmethod
    def check_password(cls, hash_password, password):
        return check_password_hash(hash_password, password)
