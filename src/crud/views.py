from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.app import db
from src.crud.forms import UserForm
from src.crud.models import User

crud = Blueprint("crud", __name__, template_folder="templates")


@crud.route("/")
@login_required
def index():
	return render_template("crud/index.html")


@crud.route("/sql")
@login_required
def sql():
	db.session.query(User).all()
	for user in users:
		print(user)
	return "check the console log"


@crud.route("/users/new", methods=["POST", "GET"])
@login_required
def create_user():
	form = UserForm()

	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data,
		)

		db.session.add(user)
		db.session.commit()

		return redirect(url_for("crud.users"))
	return render_template("crud/create.html", form=form)


@crud.route("/users")
def users():
	users = User.query.all()
	return render_template("crud/index.html", users=users)


@crud.route("/own")
@login_required
def own():
	own = User.query.filter(User.id == current_user.id).all()
	return render_template("crud/own.html", own=own)


@crud.route("/own/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
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
	flash("completely deleted")
	user = User.query.filter_by(id=user_id).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for("home.index"))
