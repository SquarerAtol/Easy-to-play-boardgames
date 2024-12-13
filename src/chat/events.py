from os import error

from flask import session
from flask_login import current_user, login_required
from flask_socketio import Namespace, emit, join_room, leave_room


class ChatNamespace(Namespace):
	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def on_event(self, data):
		emit('my response', data)

	def on_joined(self, data):
		# user의 name을 채팅 텍스트에 표시할 수 있도록 전달
		if current_user.is_authenticated:
			name = current_user.username
		else:
			name = session.get('name')
		# 공통 room 설정
		room = session.get('room')
		if room and name:
			join_room(room)
			emit('status', {'message': f'"{name}" 가 채팅에 참여합니다.'}, room=room)
		if name == '':
			emit('error', {'message': 'name missing'})
			return

	def on_text(self, data):
		# 유저의 메시지가 텍스트에 표시될 수 있도록 함
		if current_user.is_authenticated:
			name = current_user.username
		else:
			name = session.get('name')
		room = session.get('room')
		if room and name:
			emit('message', {'message': f"{name}: {data['message']}"}, room=room)
		if not data.get('message', '').strip():
			emit('error', {'message': "message missing"})
			return

	def on_left(self, data):
		# user의 연결이 끊어질 때 처리
		if current_user.is_authenticated:
			name = current_user.username
		else:
			name = session.get('name')
		room = session.get('room')
		if room and name:
			leave_room(room)
			emit('status', {'message': f'{name} has left.'}, room=room)
