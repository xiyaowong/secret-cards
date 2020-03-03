from flask import Blueprint, Flask
from flask.helpers import get_env
from flask_cors import CORS


api_bp = Blueprint('api', __name__)


def init_app(app: Flask):

    from .views import init_bp
    init_bp(api_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    # if get_env() == "development":
    #     CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app, resources={r"/api/*": {"origins": "*"}})
