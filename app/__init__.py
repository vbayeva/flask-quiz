from flask import Flask
from flask_migrate import Migrate

from .extenstions import db, login_manager
from .commands import create_tables, delete_questions, delete_users
from .routes.main import main
from .routes.auth import auth
from .models import User

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)
    app.cli.add_command(delete_questions)
    app.cli.add_command(delete_users)

    return app
