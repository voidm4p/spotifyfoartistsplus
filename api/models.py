import enum
from operator import itemgetter
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import Timestamp
from sqlalchemy_utils.types import ChoiceType, Choice
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = SQLAlchemy()

class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (Choice, lambda x: {'code': x.code, 'value': x.value}),
    )


user_spotify_user_table = db.Table('user_spotify_user', Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('spotify_user_id', db.Integer, db.ForeignKey('SpotifyUser.id')),
)

class User(db.Model, Timestamp, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))
    spotify_users = db.relationship("SpotifyUser", secondary=user_spotify_user_table, back_populates="users")


class SpotifyUser(db.Model, Timestamp, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    access_token = db.Column(db.String(200), unique=True)
    refresh_token = db.Column(db.String(200), unique=True)
    expires = db.Column(db.Integer)
    users = db.relationship("User", secondary=user_spotify_user_table, back_populates="spotify_users")

