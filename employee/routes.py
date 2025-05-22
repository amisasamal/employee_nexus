from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash
import uuid

from .forms import EmployeeRegistrationForm
from ..models.employee import submit_data, get_user_by_email

employee_bp = Blueprint('employee', __name__)

def generate_employee_id():
    return uuid.uuid4().hex[:8]  # 8-character unique string

@employee_bp.route('/')
def index():
    form = EmployeeRegistrationForm()
    formclass = 'form-control'
    
    return render_template('index.html', form=form, formclass=formclass)

@employee_bp.route('/submit', methods=['POST'])
def submit():
    form = EmployeeRegistrationForm()
    formclass = 'form-control'

    if form.validate_on_submit():
       emp_info = {
            'employee_id': generate_employee_id(),
            'salutation': form.salutation.data.strip(),
            'first_name': form.first_name.data.strip(),
            'middle_name': form.middle_name.data.strip(),
            'last_name': form.last_name.data.strip(),
            'date_of_birth': form.date_of_birth.data,
            'joined_on': form.joined_on.data,
            'post': form.post.data.strip(),
            'mobile_number': form.mobile_number.data.strip(),
            'email_id': form.email_id.data.strip(),
            'password': generate_password_hash(form.confirm_password.data.strip())
       }
        
       existing_user = get_user_by_email(emp_info['email_id'])
       if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('employee.index'))

       try:
            submit_data(emp_info) 
            flash(f"You have successfully submitted your data {emp_info['salutation']} {emp_info['first_name']}")
            return render_template('registered.html')
       except Exception as e:
            flash(f"An error occurred while saving your data. Please try again later.", "danger")
            print("Database Error:", e)  # Log the actual error in console for debugging
            return redirect(url_for('employee.index'))

    else:
        flash("There are errors in the form. Please fix them and submit again.", "danger")
        print('error', form.errors)
        return render_template('index.html', form=form, formclass=formclass)

@employee_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))

    email = session['user']['email']

    user = get_user_by_email(email)

    return render_template('dashboard.html', user=user)