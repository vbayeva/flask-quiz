import click 
from flask.cli import with_appcontext
from .extenstions import db
from .models import Questions, User

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name='delete_questions')
@with_appcontext
def delete_questions():
    db.session.query(Questions).delete()
    db.session.commit()

@click.command(name='delete_users')
@with_appcontext
def delete_users():
    db.session.query(User).delete()
    db.session.commit()