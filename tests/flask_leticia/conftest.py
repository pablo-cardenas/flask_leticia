import pytest
import tempfile
from flask_leticia import create_app
from flask_leticia.database import init_db, db_session
from flask_leticia.models import Question


@pytest.fixture
def app():
    with tempfile.NamedTemporaryFile() as db_file:
        app = create_app({
            'TESTING': True,
            'DATABASE_URI': f'sqlite:///{db_file.name}',
        })

        with app.app_context():
            init_db()

            questions = [
                Question(
                    nrow=10,
                    ncol=10,
                    params=[1, 2, 3, 4],
                    seed=42,
                    points=[1, 2, 3, 4, 5],
                    variables=[[[[]]]],
                    probabilities=[[[]]],
                ),
            ]
            db_session.add_all(questions)
            db_session.commit()

        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
