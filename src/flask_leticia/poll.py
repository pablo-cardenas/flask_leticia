from flask import Blueprint, render_template, request, Response, redirect, url_for
from flask_leticia.database import db_session
from sqlalchemy import select, insert
from flask_leticia.models import Question, Answer
from werkzeug.exceptions import abort
import json

bp = Blueprint('poll', __name__)


@bp.route('/')
def index():
    questions = db_session.execute(select(Question)).scalars().all()
    return render_template('index.html', questions=questions)


@bp.route('/question/<id>', methods=('GET', 'POST'))
def question_detail(id):
    if db_session.get(Question, id) is None:
        abort(404)

    if request.method == 'POST':
        if not ({'bad_step', 'good_squares'} <= request.form.keys()):
            abort(400)

        a = Answer(
            question_id=id,
            bad_step=request.form['bad_step'],
            good_squares=json.loads(request.form['good_squares']),
        )

        db_session.add(a)
        db_session.commit()

        return redirect(url_for('poll.index'))

    question = db_session.get(Question, id)
    return render_template('question_detail.html', question=question)


@bp.route('/api/question/<id>')
def question_get(id):
    q = db_session.get(Question, id)

    return Response(
        mimetype="application/json",
        response=json.dumps({
            'nrow': q.nrow,
            'ncol': q.ncol,
            'params': q.params,
            'seed': q.seed,
            'points': q.points,
        }),
        status=200,
    )


@bp.route('/api/question/create', methods=('POST',))
def question_create():
    data = request.json

    if not {
        'nrow',
        'ncol',
        'params',
        'seed',
        'points',
        'variables',
        'probabilities',
    } <= data.keys():
        print(list(data.keys()))
        abort(400)


    q = Question(
        nrow=data['nrow'],
        ncol=data['ncol'],
        params=data['params'],
        seed=data['seed'],
        points=data['points'],
        variables=data['variables'],
        probabilities=data['probabilities'],
    )

    if db_session.execute(select(Question).filter_by(
        nrow=q.nrow,
        ncol=q.ncol,
        params=q.params,
        seed=q.seed,
    )).first() is not None:
        return Response(
            mimetype="text/plain",
            response=f"Sorry, already in the database.\n{q.nrow=}\n{q.ncol=}\n{q.params=}\n{q.seed=}\n",
            status=409,
        )

    db_session.add(q)
    db_session.commit()

    return Response(
        mimetype="text/plain",
        response="Thanks!\n",
        status=201,
    )
