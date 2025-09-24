from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                length)


class UserForm(FlaskForm):
    username = StringField(
        "유저명",
        validators=[
            DataRequired(message="유저명을 입력"),
            length(max=12, message="12자 이내로"),
		]
	)

    email = StringField(
		"이메일 주소",
		validators=[
			DataRequired(message="이메일 주소 입력"),
			Email(message="이메일 주소를 입력할 것"),
		]
	)

    password = PasswordField(
		"새 비밀번호",
		validators=[
			DataRequired(message="비밀번호를 입력해"),
			InputRequired(),
			EqualTo('confirm', message='비밀번호 동일해야 함'),
		]
	)

    confirm = PasswordField('비밀번호 확인')

    submit = SubmitField("등록")
