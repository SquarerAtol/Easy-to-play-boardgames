from pathlib import Path

basedir = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = "ab963bce0f28acc2c3c50d84012c706469191863c901a074ec2de3b2b943"
    WTF_CSRF_SECRET_KEY = "9a1de57fcdd1a1ece57b50f7ccb80cfb065ad12f7774191a98febc0eefc3"	# flask-wtf csrf token
    UPLOAD_FOLDER = str(Path(basedir, "src", "files", "game_file"))	# 게임 파일 업로드 폴더


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    "testing": TestingConfig,
    "local": LocalConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
