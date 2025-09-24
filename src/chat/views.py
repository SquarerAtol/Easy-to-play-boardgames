from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from src.chat.forms import ChatForm

chat = Blueprint("chat", __name__, template_folder="templates")


@chat.route('/', methods=['GET', 'POST'])
def index():
    # username을 form으로 전달, room은 0으로 고정
	form = ChatForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			session['name'] = request.form.get('name', '').strip()
			session['room'] = request.form.get('room', '0').strip()

	name = session.get('name', '')
	room = session.get('room', '0')
	return render_template('chat/index.html', name=name, room=room, form=form)