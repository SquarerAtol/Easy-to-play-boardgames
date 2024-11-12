import os
import shutil
import zipfile
from pathlib import Path

from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, send_from_directory, url_for)
from flask_login import current_user, login_required
from sqlalchemy import desc
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
	games = Game.query.join(User).order_by(desc(Game.created_at)).all()

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
			file_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
			upload_file.save(file_path)

			# Handle ZIP extraction with error handling
			if upload_file.filename.lower().endswith(".zip"):
				extract_folder = Path(current_app.config['UPLOAD_FOLDER']) / filename.split(".")[0]

				# Ensure extract_folder is a directory
				extract_folder.mkdir(parents=True, exist_ok=True)
				try:
					with zipfile.ZipFile(file_path, 'r') as zip_ref:
						zip_ref.extractall(extract_folder)
					current_app.logger.info(f"ZIP file '{filename}' extracted to '{extract_folder}'")
					game = Game(
					upload_path=extract_folder.as_posix(),
					title=form.title.data,
					description=form.description.data,
					user_id=current_user.id,
					)
					db.session.add(game)
					db.session.commit()
					flash("File uploaded successfully!", "success")
				except zipfile.BadZipFile:
					flash("Uploaded file is not a valid ZIP file.", "error")
					# Optionally delete the invalid ZIP file
					file_path.unlink(missing_ok=True)
				os.remove(file_path)
			else:
				game = Game(
				upload_path=filename,
				title=form.title.data,
				description=form.description.data,
				user_id=current_user.id,
				)
				db.session.add(game)
				db.session.commit()
				flash("File uploaded successfully!", "success")
				return redirect(url_for('game.upload_file'))
			return redirect(url_for("game.index", filename=filename.split(".")[0]))

	return render_template("game/upload.html", form=form)


# Route to display the uploaded game
@game.route("home/<filename>/<int:game_id>")
def show_game(game_id, filename):
	game = Game.query.get(game_id)
	if not game:
		abort(404)
	extract_folder = Path(current_app.config['UPLOAD_FOLDER']) / filename.split(".")[0]
	index_file = extract_folder / '*.html'
	if not extract_folder.is_dir() or not index_file.is_file():
		abort(404)
	return send_from_directory(extract_folder, '*.html')


# Serve the uploaded files
@game.route('/uploads/<path:filename>')
def download_file(filename):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@game.route("<int:game_id>/delete", methods=["POST"])
@login_required
def delete_game(game_id):
	# Fetch game entry from the database
	game = Game.query.filter_by(id=game_id, user_id=current_user.id).first()

	if not game:
		flash("Game not found", "error")
		return redirect(url_for("game.index"))


	# Construct file path from the game's upload path
	file_path = Path(current_app.config['UPLOAD_FOLDER']) / game.upload_path
	extract_folder = Path(current_app.config['UPLOAD_FOLDER']) / game.upload_path.split(".")[0]

	# Attempt to delete the file if it exists
	if file_path.exists():
		try:
			os.remove(file_path)
			current_app.logger.info(f"Deleted file: {file_path}")
		except Exception as e:
			flash(f"Error deleting file: {e}", "error")
			current_app.logger.error(f"Error deleting folder {file_path}: {e}")
			return redirect(url_for("game.index"))

	if extract_folder.exists() and extract_folder.is_dir():
		try:
			shutil.rmtree(extract_folder)
			current_app.logger.info(f"Deleted folder: {extract_folder}")
		except Exception as e:
			flash(f"Error deleting file: {e}", "error")
			current_app.logger.error(f"Error deleting folder {extract_folder}: {e}")
			return redirect(url_for("game.index"))

	# Delete game entry from the database
	db.session.delete(game)
	db.session.commit()
	flash('Game deleted successfully', "success")

	return redirect(url_for("game.index"))
