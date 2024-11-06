from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from src.chat.forms import ChatForm

chat = Blueprint("chat", __name__, template_folder="templates")


@chat.route('/', methods=['GET', 'POST'])
def index():
	# Uncomment the form line if using ChatForm for validation
	# form = ChatForm()
	if request.method == 'POST':
		session['name'] = request.form.get('name', '').strip()
		session['room'] = request.form.get('room', '0').strip()  # Default room to '0' if not provided

	name = session.get('name', '')
	room = session.get('room', '0')
	return render_template('chat/index.html', name=name, room=room)