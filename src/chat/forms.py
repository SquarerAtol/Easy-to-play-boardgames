from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class ChatForm(FlaskForm):
    name = StringField(
		"유저명",
		validators=[
			DataRequired(message="check name"),
		]
	)
    
    room = StringField(
		"room number",
		validators=[
			DataRequired(message="input room number"),
			InputRequired(),
		]
	)
    
    submit = SubmitField("submit")