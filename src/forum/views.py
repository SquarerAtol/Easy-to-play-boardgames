from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from src.app import db
from src.forum.forms import PostForm
from src.forum.models import Post

forum = Blueprint("forum", __name__,
                  template_folder="templates", static_folder="static",)


@forum.route("/")
def index():
    return render_template("forum/index.html")


@forum.route("/posts/new", methods=["POST", "GET"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            username=form.username.data,
            title=form.title.data,
            body=form.body.data,
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("forum.posts"))
    return render_template("forum/create.html", form=form)


@forum.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("forum/index.html", posts=posts)


@forum.route("/posts/<post_id>", methods=["POST", "GET"])
@login_required
def edit_post(user_id):
    form = PostForm()

    post = Post.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("forum.posts"))

    return render_template("forum/edit.html", post=post, form=form)


@forum.route("posts/<post_id>/delete", methods=["POST"])
@login_required
def delete_post(user_id):
    post = Post.query.filter_by(id=user_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("forum.posts"))
