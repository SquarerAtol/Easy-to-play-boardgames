from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length


class PostForm(FlaskForm):
    title = StringField(
        "제목",
        validators=[
            DataRequired(message="제목 입력"),
            length(max=50, message="50자 이내"),
        ],
    )

    body = TextAreaField(
        "내용",
        validators=[
            DataRequired(message="내용 입력"),
            length(max=300, message="300자 이내"),
        ],
    )
    submit = SubmitField("Post")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")

