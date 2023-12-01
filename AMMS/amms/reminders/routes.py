from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from amms.models import Reminder
from amms import db
import subprocess
import time

rems = []

reminder = Blueprint('reminder', __name__)

def reminder_handler():
    while True:
        for reminder in rems:
            current_time = time.strftime("%H:%M")
            if current_time == reminder['time']:
                subprocess.run(["notify-send", "Reminder", reminder['message']])
                rems.remove(reminder)
                db.session.delete(reminder)
                db.session.commit()
        time.sleep(60)

@reminder.route('/reminderHome', methods=['GET', 'POST'])
def reminderHome():
    rems = Reminder.query.all()
    print(rems[0].message)
    return render_template('reminders.html', reminders=rems)

@reminder.route('/add_reminder', methods=['POST'])
def add_reminder():
    time = request.form.get('time')
    message = request.form.get('message')

    if time and message:
        rmndr = Reminder(reminder_datetime = time, message=message)
        db.session.add(rmndr)
        db.session.commit()
        rems.append({'time': time, 'message': message})
    
    return redirect(url_for('reminder.reminderHome'))
