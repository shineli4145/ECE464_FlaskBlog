from .db_config import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import *


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    discussion_id = db.Column(db.Integer, db.ForeignKey(
        'discussion.id', ondelete='CASCADE'))


user_discussion = db.Table('user_discussion', db.Column('user_id', db.Integer, db.ForeignKey(
    'user.id', ondelete='CASCADE')), db.Column('discussion_id', db.Integer, db.ForeignKey('discussion.id', ondelete='CASCADE')), db.UniqueConstraint('user_id', 'discussion_id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='author',
                            lazy=True)  # redunant/can query from discussions
    discussions = db.relationship(
        'Discussion', secondary=user_discussion, backref=db.backref('members', lazy='dynamic'))


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    posts = db.relationship('Note', backref='group', lazy=True)
    # password = db.Column(db.String(150))
