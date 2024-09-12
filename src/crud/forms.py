from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class UserForm(FlaskForm):
	username = StringField(
		"유저명",
		validators=[
			DataRequired(message="유저명을 입력"),
			length(max=12, message="12자 이내로"),
		],
	)

	
	email = StringField(
		"이메일 주소",
		validators=[
			DataRequired(message="이메일 주소 입력"),
			Email(message="이메일 주소를 입력할 것"),
		],
	)


	password = PasswordField(
		"비밀번호",
		validators=[
			DataRequired("비밀번호를 입력해"),
		],
	)

	submit = SubmitField("등록")