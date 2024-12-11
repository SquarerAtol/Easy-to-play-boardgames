import os
import shutil

import pytest

from src.app import create_app, db
from src.crud.models import User
from src.game.models import Game


@pytest.fixture
def fixture_app():
	app = create_app("testing")

	# db
	app.app_context().push()

	# db table
	with app.app_context():
		db.create_all()

	os.mkdir(app.config["UPLOAD_FOLDER"])

	yield app

	# clean up
	User.query.delete()
	Game.query.delete()
	shutil.rmtree(app.config["UPLOAD_FOLDER"])
	db.session.commit()

@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()