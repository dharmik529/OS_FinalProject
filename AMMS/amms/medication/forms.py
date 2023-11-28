from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from amms.models import Medication

class NewMedicationForm(FlaskForm):
    medication_name = StringField('Medication Name', validators=[DataRequired(), Length(min=1, max=250)])
    medication_dose = StringField('Dose', validators=[DataRequired()])
    medication_date = StringField('Date', validators=[DataRequired()])
    medication_time = StringField('Time', validators=[DataRequired()])
    submit = SubmitField('Enter')