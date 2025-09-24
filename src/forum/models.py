from datetime import datetime

from src.app import db


class Post(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"), 
        index=True
    )
    
    parent_id = db.Column(
        db.Integer, 
        db.ForeignKey('posts.id', ondelete='CASCADE'), 
        nullable=True,
        index=True
    )
    
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(
        db.DateTime, 
        default=datetime.now, 
        nullable=False
    )
    
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.now,
        onupdate=datetime.now, 
        nullable=False
    )
    
    user = db.relationship(
        'User', 
        backref=db.backref('posts', lazy='dynamic')
    )
    
    parent = db.relationship(
        'Post', 
        remote_side=[id], 
        backref=db.backref('replies', lazy='dynamic'),
        single_parent=True,
    )