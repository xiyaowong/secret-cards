from flask import Flask
from flask import current_app

from back_end.models import db, User, Post


def create_app(env=None) -> Flask:
    app = Flask(__name__)

    from back_end.config import config
    if not env:
        env = "development"
    app.config.from_object(config[env])

    from back_end import models
    models.init_app(app)

    from back_end import api
    api.init_app(app)

    @app.route("/")
    def hello():
        print(current_app.config['ENV'])
        return "<h1>{}</h1>".format(current_app.config['ENV'])

    @app.route("/generate_test_data")
    def a():
        from back_end import test_data
        test_data.run()
        return "OK!"

    return app


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, "Post": Post}


if __name__ == "__main__":
    app.run()
