from datetime import datetime

from src.app import db


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.Text(50), nullable=False)
    body = db.Column(db.Text(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now, nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))