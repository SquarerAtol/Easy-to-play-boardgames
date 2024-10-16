from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadGameForm(FlaskForm):
	game = FileField(
		validators=[
			FileRequired("파일을 지정하세요"),
			FileAllowed(['html', 'css', 'js', 'png', 'jpg', 'jpeg'], "지원되지 않는 파일 형식"),
		],
	)
	submit = SubmitField("Upload")


class DeleteForm(FlaskForm):
	submit = SubmitField("Delete")
