from flask import Flask
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE_URI=f'sqlite:///{app.instance_path}/leticia.db',
    )

    if test_config is not None:
        # Pass test config if passed in
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # flask_webpackext
    from flask_webpackext.project import WebpackTemplateProject
    from flask_webpackext import FlaskWebpackExt
    project = WebpackTemplateProject(
        __name__,
        project_folder='webpack',
        config_path='config.json',
    )

    app.config.update(dict(
        WEBPACKEXT_PROJECT=project,
    ))

    FlaskWebpackExt(app)

    from . import database
    database.init_app(app)

    from . import poll
    app.register_blueprint(poll.bp)

    return app
