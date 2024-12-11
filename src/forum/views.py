from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc, select

from src.app import db
from src.crud.models import User
from src.forum.forms import DeleteForm, PostForm
from src.forum.models import Post

forum = Blueprint("forum", __name__, template_folder="templates", static_folder="static"
,)


@forum.route("/")
def index():
	# forum page: 내림차순 정렬
	posts_query = (
		select(Post)
		.join(User, User.id == Post.user_id)
		.order_by(desc(Post.created_at))
	)
	posts = db.session.execute(posts_query).scalars().all()

	delete_form = DeleteForm()
	create_form = PostForm()
	
	return render_template("forum/index.html", posts=posts, delete_form=delete_form,
						create_form=create_form)


@forum.route("/create", methods=["POST", "GET"])
@login_required
def create_post():
	# post 작성
	form = PostForm()
	if request.method == 'POST':

		if form.validate_on_submit():
			post = Post(
				title=form.title.data,
				body=form.body.data,
				user_id=current_user.id,
			)
			db.session.add(post)
			db.session.commit()

			return redirect(url_for("forum.index"))
	return render_template("forum/create.html", form=form,)


@forum.route("/reply/<int:post_id>", methods=["POST", "GET"])
@login_required
def reply_post(post_id):
	# reply post
	form = PostForm()
	parent_post = Post.query.get_or_404(post_id)

	if request.method == 'POST':
		if form.validate_on_submit():
			reply = Post(
				body=form.body.data,
				user_id=current_user.id,
				parent_id=parent_post.id
			)
			db.session.add(reply)
			db.session.commit()
			
			return redirect(url_for("forum.index",post_id=parent_post.id))
	return render_template("forum/index.html",form=form, parent_post=parent_post)


@forum.route("/<int:post_id>/update", methods=["POST", "GET"])
@login_required
def edit_post(post_id):
	# post 수정
	post = Post.query.filter_by(id=post_id).first()

	if post is None:
		flash("Post not found.", "error")
		return redirect(url_for("forum.index"))

	form = PostForm(obj=post)

	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		db.session.add(post)
		db.session.commit()
		flash("updated successfully")
		return redirect(url_for("forum.index"))

	return render_template("forum/edit.html", post=post, form=form)


@forum.route("<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
	# post 삭제
	post = Post.query.filter_by(id=post_id).first()

	if not post:
		flash("Post not found", "error")
		return redirect(url_for("forum.index"))

	db.session.delete(post)
	db.session.commit()
	flash('Post deleted Successfully', "success")
	return redirect(url_for("forum.index"))
