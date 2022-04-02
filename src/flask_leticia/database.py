import click
from flask import g, current_app, Flask
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from werkzeug.local import LocalProxy


def get_db_session():
    if 'db_session' not in g:
        engine = create_engine(current_app.config['DATABASE_URI'])
        g.db_session = Session(engine)

    return g.db_session


db_session = LocalProxy(get_db_session)


def teardown_db_session(e=None):
    if 'db_session' in g:
        g.db_session.close()
        g.db_session.invalidate()
        g.db_session.get_bind().dispose()


def init_db():
    from .models import Base
    Base.metadata.create_all(db_session.get_bind())


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app: Flask):
    app.teardown_appcontext(teardown_db_session)
    app.cli.add_command(init_db_command)
