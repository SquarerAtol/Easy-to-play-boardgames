from flask import Blueprint, current_app, render_template
from sqlalchemy import desc, select

from src.app import db
from src.crud.models import User
from src.forum.forms import DeleteForm
from src.forum.models import Post
from src.game.models import Game

home = Blueprint('home', __name__, template_folder="templates", static_folder="static",)


@home.route('/')
def index():
	context = get_home_context()
	return render_template('home/index.html', **context)


@home.route('/game/<int:game_id>')
def home_game(game_id):
    # `game_id`를 통해 데이터베이스에서 해당 게임을 조회
    game = Game.query.get_or_404(game_id)  # 존재하지 않는 게임이면 404 반환

    # 로그 기록
    current_app.logger.debug(f"homegame log debug id: '{game_id}'")

    # 데이터 로드
    context = get_home_context()
    context.update({"game": game})  # `game`만 전달

    return render_template('home/index.html', **context)


def mask_email(email):
	# 이메일 마스킹 함수: 이메일 주소의 사용자 부분을 일부 *로 대체
	name, domain = email.split('@')
	if len(name) > 2:
		masked_name = name[0] + '*' * (len(name) - 2) + name[-1]
	else:
		masked_name = name[0] + '*'
	return masked_name + '@' + domain


def get_home_context():
    # 메인 로직 헬퍼 함수
    posts = (
        select(Post)
        .join(User, User.id == Post.user_id)
        .order_by(desc(Post.created_at))
    )
    result = db.session.execute(posts).scalars().all()

    users = User.query.all()
    for user in users:
        user.masked_email = mask_email(user.email)

    delete_form = DeleteForm()

    return {"posts": result, "users": users, "delete_form": delete_form}