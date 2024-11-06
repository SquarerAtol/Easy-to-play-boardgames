from flask import session
# from flask_login import current_user, login_required
from flask_socketio import Namespace, emit, join_room, leave_room


class ChatNamespace(Namespace):
	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def on_event(self, data):
		emit('my response', data)

	def on_joined(self, data):
		room = session.get('room')
		name = session.get('name')
		if room and name:
			join_room(room)
			emit('status', {'message': f'{name} has joined.'}, room=room)

	def on_text(self, data):
		room = session.get('room')
		name = session.get('name')
		if room and name:
			emit('message', {'message': f"{name}: {data['message']}"}, room=room)

	def on_left(self, data):
		room = session.get('room')
		name = session.get('name')
		if room and name:
			leave_room(room)
			emit('status', {'message': f'{name} has left.'}, room=room)

	# @login_required
	# def connect_handler(self):
	# 	if current_user.is_authenticated:
	# 		emit('my response', {'message:': '{0} has joined.'
	# 							 .format(current_user.id)}, broadcast=True)
	# 	else:
	# 		return False
