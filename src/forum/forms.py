from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length


class PostForm(FlaskForm):
    title = StringField(
        "제목",
        validators=[
            DataRequired(message="제목 입력"),
            length(max=20, message="20자 이내"),
        ],
    )

    body = TextAreaField(
        "내용",
        validators=[
            DataRequired(message="내용 입력"),
            length(max=200, message="200자 이내"),
        ],
    )
    submit = SubmitField("Post")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")

