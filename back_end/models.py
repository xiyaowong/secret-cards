from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


db: SQLAlchemy = SQLAlchemy()


# likes = db.Table(
#     'likes',
#     db.Column('liked_id', db.Integer, db.ForeignKey('posts.id')),
#     db.Column('liker_id', db.Integer, db.ForeignKey('users.id')),
# )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, nullable=True, unique=True)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(60), default="")
    gender = db.Column(db.String, default="保密")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Integer, default=0)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    # likeds = db.relationship(
    #     'Post', secondary=likes,
    #     primaryjoin=(likes.c.liker_id == id),
    #     backref=db.backref('likeds', lazy='dynamic'),
    #     lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "gender": self.gender,
            "is_active": self.is_active,
            "date": self.date,
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def generate_token(self, exprires_in=3*24*60*60):  # 3d
        s = Serializer(
            current_app.config['SECRET_KEY'], expires_in=exprires_in)
        payload = {"id": self.id}
        token = s.dumps(payload).decode("utf-8")
        return token

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            return data
        except:
            return None


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # views = db.Column(db.Integer, default=0)
    # likers = db.relationship(
    #     'Post', secondary=likes,
    #     primaryjoin=(likes.c.liked_id == id),
    #     backref=db.backref('likers', lazy='dynamic'),
    #     lazy='dynamic')

    def to_dict(self):
        data = {
            "id": self.id,
            "author_id": self.author_id,
            "content": self.content,
            "date": self.date,
        }
        return data


def init_app(app):
    db.init_app(app)
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
