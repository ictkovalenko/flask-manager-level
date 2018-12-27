from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Roles:
    USER = 1
    USER_NAME = u'user'

    MANAGER = 2
    MANAGER_NAME = u'manager'

    ADMIN = 3
    ADMIN_NAME = u'admin'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    name_first = db.Column(db.String(128), nullable=False)
    name_last = db.Column(db.String(128), nullable=False)
    name_middle = db.Column(db.String(128))
    last_login_date = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.Integer, default=Roles.USER)
    has_password = db.Column(db.Boolean, default=False)
    company = db.Column(db.String(255))
    city = db.Column(db.String(255))
    contacts = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password issue')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        if self.is_administrator:
            return Roles.ADMIN_NAME
        elif self.is_manager:
            return Roles.MANAGER_NAME
        else:
            return Roles.USER_NAME

    @property
    def is_administrator(self):
        return self.role == Roles.ADMIN

    @property
    def is_manager(self):
        return self.role == Roles.MANAGER

    @property
    def is_user(self):
        return self.role == Roles.USER

    def __repr__(self):
        return '<User: {}>'.format(self.login)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
