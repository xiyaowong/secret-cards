import os

from dotenv import load_dotenv


here = os.path.abspath(os.path.dirname(__file__))

load_dotenv(verbose=True)


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or "how-awesome-it-is"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///" + os.path.join(here, "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}