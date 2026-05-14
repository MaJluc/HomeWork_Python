from app.extensions import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    questions = db.relationship(
        'Question',
        backref='category',
        lazy='select',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Category: {self.name}'


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    responses = db.relationship(
        'Response',
        backref='question',
        lazy='select',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Question: {self.text}'


class Statistic(db.Model):
    __tablename__ = 'statistic'

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return (
            f'Statistic(question_id={self.question_id}, '
            f'agree={self.agree_count}, '
            f'disagree={self.disagree_count})'
        )