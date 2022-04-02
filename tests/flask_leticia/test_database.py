from flask_leticia.database import get_db_session


def test_get_close_db(app):
    with app.app_context():
        db_sess = get_db_session()
        assert db_sess is get_db_session()


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flask_leticia.database.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.\n' == result.output
    assert Recorder.called
