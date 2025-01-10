import os
from flask import Flask

def register_blueprints(app: Flask):
    from . import routes
    print("Registering blueprints...")
    app.register_blueprint(routes.blueprint)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev"
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print("Flask instance created!")
    app.app_context().push()
    return app

app = create_app()
register_blueprints(app)
