from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
	username = StringField(
		"유저명",
		validators=[
			DataRequired(message="유저명을 입력"),
			Length(1, 12, message="12자 이내"),
		],
	)
	email = StringField(
		"이메일 주소",
		validators=[
			DataRequired(message="이메일 입력"),
			Email(message="이메일 형식을 지키세요"),
		],
	)
	password = PasswordField(
		"비밀번호",
		validators=[
			DataRequired(message="비밀번호 입력"),
		],
	)
	submit = SubmitField("submit")


class LoginForm(FlaskForm):
	email = StringField(
		"이메일 주소",
		validators=[
			DataRequired(message="이메일 입력"),
			Email(message="이메일 형식 지켜"),
		],
	)
	password = PasswordField(
		"비밀번호",
		validators=[
			DataRequired(message="비밀번호 입력"),
		],
	)
	submit = SubmitField("log in")
