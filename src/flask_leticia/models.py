from sqlalchemy import Column, JSON, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, deferred


Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    nrow = Column(Integer, nullable=False)
    ncol = Column(Integer, nullable=False)
    params = Column(JSON, nullable=False)
    seed = Column(Integer, nullable=False)
    points = deferred(Column(JSON, nullable=False))
    variables = deferred(Column(JSON, nullable=False))
    probabilities = deferred(Column(JSON, nullable=False))

    answers = relationship('Answer', back_populates='question')


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    bad_step = Column(Integer, nullable=False)
    good_squares = Column(JSON, nullable=False)

    question = relationship('Question', back_populates='answers')
