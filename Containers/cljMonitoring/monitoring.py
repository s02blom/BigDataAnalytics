import os
from time import sleep
from flask import Flask
from .timers import CollectionTimer
from .db import get_connection

COLLECTIONS = ["files", "chunks", "candidates", "clones"]

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

def main():
    app = create_app()
    register_blueprints(app)
    print("Sleeping to wait for database start up", flush=True)
    sleep(15)   # Sleeping for 15s to ensure that the database has had time to start up
    timers = {}
    for name in COLLECTIONS:
        new_connection = get_connection()
        timer = CollectionTimer(collection_name=name, database=new_connection, interval=os.environ.get("SAMPLE_RATE"))
        timer.start()
        timers[name] = timer

    return app

main()