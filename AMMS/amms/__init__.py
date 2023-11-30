from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from amms.config import Config
import threading



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from amms.users.routes import users
    from amms.main.routes import main
    from amms.medication.routes import medication
    from amms.reminders.routes import reminder_handler, reminder
    #from amms.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(medication)
    app.register_blueprint(reminder)

    # Start the reminder thread
    reminder_thread = threading.Thread(target=reminder_handler)
    reminder_thread.start()
    
    return app
