import bcrypt
from ...lib import db, Serializer


class User(db.Model, Serializer):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(128))
    enabled = db.Column(db.Boolean())
    timezone = db.Column(db.String(32), nullable=False, default='UTC')
    language = db.Column(db.String(4), nullable=False, default='ZZ')
    image_url = db.Column(db.Text, nullable=True)

    def __init__(self, user_obj):
        self.user_id = user_obj['user_id']
        self.email = user_obj['email']
        self.password = user_obj['password']
        self.name = user_obj['name']
        self.enabled = user_obj['enabled']
        self.timezone = user_obj['timezone']
        self.language = user_obj['language']
        self.image_url = user_obj['image_url']

    def hash_password(self, _password):
        self.password = bcrypt.hashpw(str.encode(_password), bcrypt.gensalt())

    def check_password(self, _password):
        return bcrypt.checkpw(str.encode(_password), str.encode(self.password))

    @classmethod
    def email_exist(cls, _email):
        _usr = User.query.filter_by(email=_email).first()

        if _usr:
            return True
        return False
