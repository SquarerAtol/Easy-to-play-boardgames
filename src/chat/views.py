from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from src.chat.forms import ChatForm

chat = Blueprint("chat", __name__, template_folder="templates")


@chat.route('/', methods=['GET', 'POST'])
def index():
    # Uncomment the form line if using ChatForm for validation
    # form = ChatForm()
    if request.method == 'POST':
        # Get user name and room from form submission
        session['name'] = request.form.get('name', '').strip()
        session['room'] = request.form.get('room', '').strip()
        
        # Redirect to 'create' route if name and room are provided
        if session['name'] and session['room']:
            return redirect(url_for('chat.create'))
        
    # Render the chat index page
    return render_template('chat/index.html')  #, form=form if using form


@chat.route('/create')
def create():
    # Retrieve name and room from session
    name = session.get('name', '')
    room = session.get('room', '')

    # Redirect to index if either name or room is missing
    if not name or not room:
        return redirect(url_for('chat.index'))
    
    # Render the chat room page with name and room
    return render_template('chat/create.html', name=name, room=room)