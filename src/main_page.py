from flask import Blueprint, render_template

from src.db import get_db

bp = Blueprint('main_page', __name__)

@bp.route('/')
def main():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, p.title, p.body, p.created, user_id, userId'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' ORDER BY p.created DESC'
    ).fetchall()
    return render_template('mainpage/main_page.html', posts=posts)