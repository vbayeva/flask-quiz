from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extenstions import db 

user_questions = db.Table('user_questions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(100))
    nickname = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean)
    main_score = db.Column(db.Integer)

    answered_questions = db.relationship('Questions', secondary=user_questions,
                                         backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def unhashed_password(self):
        return AttributeError('Nie możesz zobaczyć nieszyfrowane hasło!')
    
    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(350), unique=True)
    first_option = db.Column(db.String(100))
    second_option = db.Column(db.String(100))
    third_option = db.Column(db.String(100))
    fourth_option = db.Column(db.String(100))
    answer = db.Column(db.String(100))

    def __repr__(self):
        return '<Question: {}>'.format(self.question)
    

