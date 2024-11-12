from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, length


class UploadGameForm(FlaskForm):
	game = FileField(
		"file",
		validators=[
			FileRequired("파일을 지정하세요"),
			FileAllowed(['zip', 'html', 'css', 'js', 'png', 'jpg', 'jpeg'], "지원되지 않는 파일 형식"),
		],
	)
	title = StringField(
		"title",
		validators=[
			DataRequired(message="제목 입력"),
			length(max=20, message="20자 이내"),
		],
	)
	description = TextAreaField(
		"description",
		validators=[
			DataRequired(message="내용 입력"),
			length(max=200, message="200자 이내"),
		],
	)
	submit = SubmitField("Upload")


class DeleteForm(FlaskForm):
	submit = SubmitField("Delete")
