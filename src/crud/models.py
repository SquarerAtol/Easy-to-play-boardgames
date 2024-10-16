from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src.app import db, login_manager


class User(db.Model, UserMixin):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(12), index=True, nullable=False)
	email = db.Column(db.String(100), unique=True, index=True, nullable=False)
	password_hash = db.Column(db.String)
	created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now, nullable=False)

	@property
	def password(self):
		raise AttributeError("비밀번호 오류")

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def is_duplicate_email(self):
		return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)
