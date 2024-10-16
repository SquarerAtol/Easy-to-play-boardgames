from datetime import datetime

from src.app import db


class Game(db.Model):
	__tablename__ = "games"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	filename = db.Column(db.String(255), nullable=False)
	title = db.Column(db.Text(20), nullable=False)
	description = db.Column(db.Text(100), nullable=False)
	upload_path = db.Column(db.String(255),nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.now,
						   onupdate=datetime.now, nullable=False)
	user = db.relationship('User', back_populates='games')
