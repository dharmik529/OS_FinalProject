from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from amms.models import Reminder
from amms import db
import subprocess
import time

reminders = []

reminder = Blueprint('reminder', __name__)

def reminder_handler():
    while True:
        for reminder in reminders:
            current_time = time.strftime("%H:%M")
            if current_time == reminder['time']:
                subprocess.run(["notify-send", "Reminder", reminder['message']])
                reminders.remove(reminder)
        time.sleep(60)

@reminder.route('/reminderHome', methods=['GET', 'POST'])
def reminderHome():
    page = request.args.get('page', 1, type=int)
    rems = Reminder.query.order_by(Reminder.id)
    return render_template('reminders.html', reminders=reminders)

@reminder.route('/add_reminder', methods=['POST'])
def add_reminder():
    time = request.form.get('time')
    message = request.form.get('message')

    if time and message:
        rmndr = Reminder(reminder_datetime = time, message=message)
        db.session.add(rmndr)
        db.session.commit()
        reminders.append({'time': time, 'message': message})
    
    return redirect(url_for('reminder.reminderHome'))
