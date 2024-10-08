from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length


class PostForm(FlaskForm):
    title = StringField(
        "title",
        validators=[
            DataRequired(message="제목 입력"),
            length(max=30, message="30자 이내"),
        ],
    )

    body = TextAreaField(
        "내용",
        validators=[
            DataRequired(message="내용 입력"),
            length(max=1000, message="1000자 이내"),
        ],
    )
    submit = SubmitField("등록")
