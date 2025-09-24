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

	games = Game.query.join(User).order_by(desc(Game.created_at)).all()

	delete_form = DeleteForm()

	return render_template('game/index.html', games=games,
						   delete_form=delete_form)


@game.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    # 게임 업로드 함수
	form = UploadGameForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			upload_file = form.game.data

			# 업로드할 파일명 암호화
			filename = secure_filename(upload_file.filename)
			file_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
			upload_file.save(file_path)

			# zip 파일을 폴더로 압축 해제
			if filename.lower().endswith(".zip"):
				extract_folder = Path(current_app.config['UPLOAD_FOLDER']) / filename.split(".")[0]
				# 중복된 게임 파일일 경우 에러 처리
				if extract_folder.exists():
					flash("파일이 이미 존재합니다.")
					os.remove(file_path)
					return redirect(url_for('game.upload_file'))
				try:
					# zip 파일의 하위 디렉토리 모두 압축 해제
					extract_folder.mkdir(parents=True, exist_ok=True)
					with zipfile.ZipFile(file_path, 'r') as zip_ref:
						zip_ref.extractall(extract_folder)
					# current_app.logger.info(f"ZIP file '{filename}' extracted to '{extract_folder}'")

					game = Game(
					upload_path=extract_folder.as_posix(),
					title=form.title.data,
					description=form.description.data,
					user_id=current_user.id,
					)

					db.session.add(game)
					db.session.commit()
					flash("파일을 성공적으로 업로드 했습니다.", "success")

				except zipfile.BadZipFile:
					# 잘못된 zip파일을 에러처리하고 경로에서 삭제
					flash("잘못된 zip파일입니다.", "error")
					file_path.unlink(missing_ok=True)
					return redirect(url_for('game.upload_file'))
 
				finally:
					# 압축 해제가 완료되어 업로드 된 원본 zip파일 삭제
					file_path.unlink(missing_ok=True)

				return redirect(url_for("game.index", game_id=game.id))
			else:
				game = Game(
				upload_path=filename,
				title=form.title.data,
				description=form.description.data,
				user_id=current_user.id,
				)
				db.session.add(game)
				db.session.commit()
				flash("파일을 성공적으로 업로드 했습니다", "success")
				# current_app.logger.info(f"'{filename}', path: '{file_path}'")
				return redirect(url_for('game.index', game_id=game.id))
	return render_template("game/upload.html", form=form)

@game.route("/show/<int:game_id>/<path:filename>")
def show_game(game_id, filename="index.html"):
    # 게임을 메인페이지에 출력하는 함수
	game = Game.query.get_or_404(game_id)
	extract_folder = Path(current_app.config['UPLOAD_FOLDER']) / game.upload_path.split(".")[0]
	if extract_folder.is_dir():
		# extract_folder 안의 index.html을 찾아 실행
		file_path = extract_folder / filename
		if file_path.exists():
			return send_from_directory(extract_folder, filename)
		else:
			abort(404, description="압축 파일 내 index.html 파일이 없음.")
	# index.html 단일 파일 바로 실행
	else:
		return send_from_directory(current_app.config['UPLOAD_FOLDER'], game.upload_path)
	abort(404, description="File not found.")

@game.route('/download/<path:path>')
def download_file(path):
	# 경로 유효성 검사 및 파일 존재 여부 확인
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], path, as_attachment=True)

@game.route("<int:game_id>/delete", methods=["POST"])
@login_required
def delete_game(game_id, filename="index.html"):
    # 게임 삭제 함수: user_id를 참조하여 게임을 찾아 삭제
	game = Game.query.filter_by(id=game_id, user_id=current_user.id).first()

	if not game:
		flash("파일을 찾을 수 없습니다.", "error")
		return redirect(url_for("game.index"))

	file_path = Path(current_app.config['UPLOAD_FOLDER']) / game.upload_path
	extract_folder = Path(current_app.config['UPLOAD_FOLDER']) / game.upload_path.split(".")[0]

	# 압축 해제된 파일을 game_file folder에서 삭제
	if file_path.exists() and file_path.is_dir():
		try:
			shutil.rmtree(file_path)
			# current_app.logger.info(f"Deleted folder: {file_path}")
		except Exception as e:
			flash(f"Error deleting directory: {e}", "error")
			# current_app.logger.error(f"Error deleting extract_folder {file_path}: {e}")
			return redirect(url_for("game.index"))
	# 단일 파일을 game_file folder에서 삭제
	else:
		try:
			os.remove(file_path)
			# current_app.logger.info(f"Deleted file: {file_path}")
		except Exception as e:
			flash(f"Error deleting file: {e}", "error")
			# current_app.logger.error(f"Error deleting nonzip_file {file_path}: {e}")
			return redirect(url_for("game.index"))

	# DB에서 삭제
	db.session.delete(game)
	db.session.commit()
	flash('Game deleted successfully', "success")

	return redirect(url_for("game.index"))
