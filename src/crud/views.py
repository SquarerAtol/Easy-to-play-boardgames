from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.app import db
from src.crud.forms import UserForm
from src.crud.models import User

crud = Blueprint("crud", __name__, template_folder="templates", static_folder="static",)


@crud.route("/")
@login_required
def index():
	return render_template("crud/index.html")


@crud.route("/users")
def users():
    # 가입한 모든 유저를 표시하는 함수
	users = User.query.all()
	for user in users:
		user.masked_email = mask_email(user.email)
	return render_template("crud/index.html", users=users)


def mask_email(email):
	# 이메일 마스킹 함수: 이메일 주소의 사용자 부분을 일부 *로 대체
	name, domain = email.split('@')
	if len(name) > 3:
		masked_name = name[0] + '*' * (len(name) - 2) + name[-1]
	else:
		masked_name = name[0] + '*'
	return masked_name + '@' + domain

@crud.route("/own")
@login_required
def own():
	# 유저 개인 페이지
	own = User.query.filter(User.id == current_user.id).all()
	return render_template("crud/own.html", own=own)

@crud.route("/own/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
	# 유저의 개인 정보를 수정
	form = UserForm()

	user = User.query.filter_by(id=user_id).first()

	if form.validate_on_submit():
		user.username = form.username.data
		user.email = form.email.data
		user.password = form.password.data
		db.session.add(user)
		db.session.commit()
		flash("update complete")
		return redirect(url_for("crud.own"))

	return render_template("crud/edit.html", user=user, form=form)


@crud.route("own/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    # 유저 삭제
	flash("completely deleted")
	user = User.query.filter_by(id=user_id).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for("home.index"))
