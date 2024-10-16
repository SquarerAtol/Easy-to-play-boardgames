import os
import zipfile
from pathlib import Path

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_from_directory, url_for)
from flask_login import current_user, login_required
from sqlalchemy import desc, select
from werkzeug.utils import secure_filename

from src.app import db
from src.crud.models import User
from src.game.forms import DeleteForm, UploadGameForm
from src.game.models import Game

game = Blueprint("game", __name__, static_folder="static", template_folder="templates")


@game.route('/')
def index():
	# games_query = (
    # 	select(Game)
	# 	.join(User, User.id == Game.user_id)
	# 	.order_by(desc(Game.created_at))
	# )
	# games = db.session.execute(games_query).all()
	games = Game.query.all()

	delete_form = DeleteForm()

	return render_template('game/index.html', games=games,
						   delete_form=delete_form)


@game.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
	form = UploadGameForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			upload_file = form.game.data

			filename = secure_filename(upload_file.filename)
			file_path = Path(current_app.config['UPLOAD_FOLDER'], filename)
			upload_file.save(file_path)

			game = Game(
			upload_path=filename,
			title=form.title.data,
			description=form.description.data,
			user_id=current_user.id,
			)
			db.session.add(game)
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
@game.route("/<filename>/<int:game_id>")
def show_game(filename, game_id):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


# Serve the uploaded files
@game.route('/uploads/<path:filename>')
def download_file(filename):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@game.route("<int:game_id>/delete", methods=["POST"])
@login_required
def delete_game(game_id):
	game = Game.query.filter_by(id=game_id).first()

	if not game:
		flash("Game not found", "error")
		return redirect(url_for("game.index"))

	db.session.delete(game)
	db.session.commit()
	flash('Game deleted Successfully', "success")
	return redirect(url_for("game.index"))

