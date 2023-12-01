from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

from amms import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication_name = db.Column(db.String(250), nullable=False)
    medication_dose = db.Column(db.Integer, nullable=False)
    medication_date = db.Column(db.Date, nullable=False)
    medication_time = db.Column(db.Time, nullable=False)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder_datetime = db.Column(db.String(50))
    message = db.Column(db.String(250))