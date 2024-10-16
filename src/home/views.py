from flask import Blueprint, render_template
from sqlalchemy import desc, select

from src.app import db
from src.crud.models import User
from src.forum.forms import DeleteForm
from src.forum.models import Post
from src.game.models import Game

home = Blueprint('home', __name__, template_folder="templates", static_folder="static",)


@home.route('/')
def index():

	game = Game.query.filter_by(id=1).first()

	posts = (
		select(Post)
		.join(User, User.id == Post.user_id)
		.order_by(desc(Post.created_at))
	)
	result = db.session.execute(posts).scalars().all()

	users = User.query.all()

	delete_form = DeleteForm()

	return render_template('home/index.html', game=game, posts=result,
						users=users, delete_form=delete_form)