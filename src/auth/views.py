from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from src.app import db
from src.auth.forms import LoginForm, RegisterForm
from src.crud.models import User

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static",)


@auth.route("/")
def index():
	return render_template("auth/index.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data,
		)

		if user.is_duplicate_email():
			flash("이메일 중복")
			return redirect(url_for("auth.register"))

		db.session.add(user)
		db.session.commit()

		login_user(user)

		next_ = request.args.get("next")
		if next_ is None or not next_.startswith("/"):
			next_ = url_for("home.index")
		return redirect(next_)

	return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for("home.index"))
		flash("이메일 or 비밀번호 오류")
	return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("auth.login"))
