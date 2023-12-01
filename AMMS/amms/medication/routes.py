from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from amms import db
from amms.medication.forms import (NewMedicationForm)
from amms.models import Medication

medication = Blueprint('medication', __name__)

@medication.route("/allMed", methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    meds = Medication.query.order_by(Medication.id).paginate(page=page, per_page=5)
    return render_template('meds.html', meds=meds)

@medication.route("/newMed", methods=['GET', 'POST'])
def newMedication():
    form = NewMedicationForm()
    if form.validate_on_submit():
        medication = Medication(medication_name=form.medication_name.data, medication_dose=form.medication_dose.data, medication_date=form.medication_date.data, medication_time=form.medication_time.data)
        db.session.add(medication)
        db.session.commit()
        flash('Your Medication was created', 'success')
        return redirect(url_for('medication.home'))
    return render_template('newMedication.html', title='Register', form=form)

@medication.route("/deleteMed/<int:id>", methods=['GET', 'POST'])
def delMedication():
    medication = Medication.query.get_or_404(id)

    db.session.delete(medication)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('medication.home'))