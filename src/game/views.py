import os
import zipfile
from pathlib import Path

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   send_from_directory, url_for)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from src.app import db
from src.crud.models import User
from src.game.forms import DeleteForm, UploadGameForm
from src.game.models import Game

game = Blueprint("game", __name__, static_folder="static", template_folder="templates")


@game.route('/')
def index():
	games = (
		db.session.query(User, Game).join(Game, User.id == Game.user_id).all()
	)
	delete_form = DeleteForm()

	return render_template('game/index.html', games=games,
						   delete_form=delete_form)


@game.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload_file():
	form = UploadGameForm()
	if form.validate_on_submit():
		upload_file = form.game.data

		filename = secure_filename(upload_file.filename)
		file_path = Path(current_app.config['UPLOAD_FOLDER'], filename)
		upload_file.save(file_path)

		user_game = Game(user_id=current_user.id, upload_path=filename)
		db.session.add(user_game)
		db.session.commit()
		flash("File uploaded successfully!", "success")

		if upload_file and upload_file.filename.lower().endswith(".zip"):
			filename = secure_filename(upload_file.filename)
			file_path = Path(current_app.config['UPLOAD_FOLDER'], filename)
			upload_file.save(file_path)

			# Extract ZIP
			extract_folder = Path(current_app.config['UPLOAD_FOLDER'], filename.split(".")[0])
			with zipfile.ZipFile(file_path, 'r') as zip_ref:
				zip_ref.extractall(extract_folder)

			os.remove(file_path)  # Remove the original ZIP file
			flash("Game uploaded successfully!", "success")
			return redirect(url_for("game.index", filename=filename.split(".")[0]))
		return redirect(url_for('game.index'))

	return render_template("game/upload.html", form=form)


# Route to display the uploaded game
@game.route("/<filename>")
def show_game(filename):
	return send_from_directory(Path(current_app.config['UPLOAD_FOLDER'], filename),
							   "home/index.html")


# Serve the uploaded files
@game.route('/uploads/<path:filename>')
def download_file(filename):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
