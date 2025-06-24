from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import datetime, date

# Import your database functions with correct filename
from ..db_models.auth_db import get_user_by_email
from ..db_models.attendance_db import (
    clock_in_employee,
    clock_out_employee, 
    get_today_attendance,
    get_employee_attendance_history
)

attendance = Blueprint('attendance', __name__)

@attendance.route('/dashboard')
def dashboard():
    # Check if user is logged in - Updated session access
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    # Get user data from session - Updated to use session['user']
    user_email = session['user']['email']
    employee_id = session['user']['employee_id']
    
    # Get full user data
    user = get_user_by_email(user_email)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))
    
    # Get today's attendance
    today_attendance = get_today_attendance(employee_id)
    
    # Get recent attendance history
    recent_attendance = get_employee_attendance_history(employee_id, 7)
    
    return render_template('attendance/dashboard.html',
                         today_attendance=today_attendance,
                         recent_attendance=recent_attendance,
                         user=user,
                         current_date=date.today())

@attendance.route('/clock-in', methods=['POST'])
def clock_in():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    employee_id = session['user']['employee_id']  # Get from session directly
    
    success, message = clock_in_employee(employee_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'warning')
    
    return redirect(url_for('attendance.dashboard'))

@attendance.route('/clock-out', methods=['POST'])
def clock_out():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    employee_id = session['user']['employee_id']  # Get from session directly
    
    success, message = clock_out_employee(employee_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'warning')
    
    return redirect(url_for('attendance.dashboard'))