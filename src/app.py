import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from src.config import config


db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.register"
login_manager.login_message = ""


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config[config_key])
	
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from src.crud import views as crud_views
    app.register_blueprint(crud_views, url_prefix="/crud")

    from src.auth import views as auth_views
    app.register_blueprint(auth_views, url_prefix="/auth")

    from . import forum
    app.register_blueprint(forum.bp)

    from . import main_page
    app.register_blueprint(main_page.bp)
    app.add_url_rule('/', endpoint='main_page')
    
    return app