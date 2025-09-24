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
    # 회원가입: username, email, password을 form으로 전달
	form = RegisterForm()

	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data,
		)

		# 이메일 중복을 검사
		if user.is_duplicate_email():
			flash("이메일 중복")
			return redirect(url_for("auth.register"))

		db.session.add(user)
		db.session.commit()

		# 로그인 상태로 연결
		login_user(user)

		next_ = request.args.get("next")	# user 데이터를 http get할 때 상태 처리
		if next_ is None or not next_.startswith("/"):
			next_ = url_for("home.index")
		return redirect(next_)

	return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # 로그인: user를 db에서 찾아 표시
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		# password를 검사하고 로그인 상태로 연결
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for("home.index"))
		flash("이메일 or 비밀번호 오류")
	return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    # 로그아웃
	logout_user()
	flash("Logged out")
	return redirect(url_for("home.index"))
