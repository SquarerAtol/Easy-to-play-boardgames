from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from src.config import config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.register"
login_manager.login_message = ""
socketio = SocketIO(logger=True, engineio_logger=True)


def create_app(config_key):
	app = Flask(__name__)
	app.config.from_object(config[config_key])

	db.init_app(app)
	Migrate(app, db)
	csrf.init_app(app)
	login_manager.init_app(app)
	socketio.init_app(app)		# socket run

	from src.crud.views import crud
	app.register_blueprint(crud, url_prefix="/crud")

	from src.auth.views import auth
	app.register_blueprint(auth, url_prefix="/auth")

	from src.home import views as home_views
	app.register_blueprint(home_views.home)

	from src.game.views import game
	app.register_blueprint(game, url_prefix="/game")

	from src.forum.views import forum
	app.register_blueprint(forum, url_prefix="/forum")

	from src.chat.views import chat
	app.register_blueprint(chat, url_prefix="/chat")

	from src.chat.events import ChatNamespace
	socketio.on_namespace(ChatNamespace('/chat'))

	@app.route("/", methods=["GET"])
	def main():
		return render_template("home/index.html")

	return app


if __name__ == "__chat__":
	config_key = "local"  # Adjust this to use an environment variable if needed
	app = create_app(config_key)
	socketio.run(app, host="127.0.0.1", port=5002, debug=True)
