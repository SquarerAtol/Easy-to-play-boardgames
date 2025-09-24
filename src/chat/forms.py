from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length


class ChatForm(FlaskForm):
    name = StringField(
		"유저명",
		validators=[
			DataRequired(message="유저명을 입력"),
			length(max=12, message="12자 이내로"),
		]
	)

    
    submit = SubmitField("submit")