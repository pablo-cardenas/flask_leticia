import json
from flask_leticia.database import db_session
from flask_leticia.models import Question


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_question_detail(client):
    response = client.get('/question/1')
    assert response.status_code == 200


def test_api_question_get(client):
    response = client.get('/api/question/1')
    assert response.status_code == 200


def test_api_question_create(client, app):
    response = client.post('/api/question/create', data=json.dumps({
            'ncol': 10,
            'nrow': 10,
            'params': [1, 2, 3, 4],
            'seed': 42,
            'points': [1, 2, 3, 4, 5, 6, 7, 8],
            'variables': [[[[]]]],
            'probabilities': [[[]]],
        }),
        content_type="application/json"
    )
    assert response.status_code == 409

    response = client.post('/api/question/create', data=json.dumps({
            'ncol': 10,
            'nrow': 10,
            'params': [0, 1, -1, -1],
            'seed': 42,
            'points': [1, 2, 3, 4, 5, 6, 7, 8],
            'variables': [[[[]]]],
            'probabilities': [[[]]],
        }),
        content_type="application/json"
    )
    assert response.status_code == 201

    with app.app_context():
        q = db_session.get(Question, 2)

        assert q.ncol == 10
        assert q.nrow == 10
        assert q.params == [0, 1, -1, -1]
        assert q.seed == 42
        assert q.points == [1, 2, 3, 4, 5, 6, 7, 8]
        assert q.variables == [[[[]]]]
        assert q.probabilities == [[[]]]


def test_api_answer_create(client):
    response = client.post('/question/1', data={
        'bad_step': 20,
        'good_squares': '[10,11,12,13,14,15]',
    })

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
