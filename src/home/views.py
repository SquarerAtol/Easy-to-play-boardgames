from flask import Blueprint, render_template
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from src.crud.models import User
from src.forum.models import Post

home = Blueprint('home', __name__, template_folder="templates", static_folder="static",)


@home.route('/')
def index():
    return render_template("home/base.html")

	# posts_query = (
	# 	select(User)
	# 	.join(Post, User.id == Post.user_id)
	# 	.order_by(desc(User.created_at))
	# )

	# session = Session()
	# result = session.execute(posts_query).scalars().all()

	# return render_template('home/index.html', posts=result)
