from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from amms.config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from amms.users.routes import users
    from amms.main.routes import main
    from amms.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
