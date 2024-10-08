from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

game = Blueprint("game", __name__, static_folder="static", template_folder="templates")


@game.route('/')
def index():
	return render_template('game/index.html')


@game.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload_file():
	if request.method == 'POST':
		upload_file = request.files['file']
		if upload_file.filename != '':
			upload_file.save(upload_file.filename)
		return redirect(url_for('game.index'))
	return render_template("game/upload.html")
