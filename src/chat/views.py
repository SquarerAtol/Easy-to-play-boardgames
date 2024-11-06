from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from src.chat.forms import ChatForm

chat = Blueprint("chat", __name__, template_folder="templates", static_folder="static")


@chat.route('/', methods=['GET', 'POST'])
def index():
    # Uncomment the form line if using ChatForm for validation
    # form = ChatForm()
	session['name'] = request.form.get('name', '').strip()
	name = session.get('name', '')
	room = 'main_room'
	return render_template('chat/index.html', name=name, room=room)