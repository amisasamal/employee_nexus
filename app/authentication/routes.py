from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message

from .forms import LoginForm, ForgotPasswordForm, ResetPasswordForm, OTPVerificationForm
from ..db_models.auth_db import get_user_by_email, update_password
from ..db_models.verify_otp_db import generate_otp, store_otp, verify_otp
from .. import mail, s

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    formclass = 'form-control'

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'email': user['email_id'],
                'employee_id': user['employee_id']
            }

            return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form, formclass=formclass)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    formclass = 'form-control'

    if form.validate_on_submit():
        email = form.email.data.strip()
        user = get_user_by_email(email)

        if user:
            # Generate and store OTP
            otp_code = generate_otp()
            if store_otp(email, otp_code):
                # Send OTP via email
                try:
                    msg = Message("Password Reset OTP", recipients=[email])
                    msg.body = f"""Hi {user['first_name']},

Your password reset OTP is: {otp_code}

This OTP is valid for 10 minutes and can be used only once.

If you didn't request this, please ignore this email.

Best regards,
Employee Nexus Team"""
                    mail.send(msg)
                    
                    # Store email in session for OTP verification
                    session['reset_email'] = email
                    flash("OTP has been sent to your email. Please check and enter it below.", "success")
                    return redirect(url_for('auth.verify_otp_route'))  # Fixed this line
                    
                except Exception as e:
                    print("Mail Error:", e)
                    flash("There was an issue sending the OTP. Try again later.", "danger")
            else:
                flash("Failed to generate OTP. Please try again.", "danger")
        else:
            flash("Email ID not found.", "danger")

    return render_template('forgot_password.html', form=form, formclass=formclass)

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp_route():
    if 'reset_email' not in session:
        flash("Please start the password reset process again.", "warning")
        return redirect(url_for('auth.forgot_password'))
    
    form = OTPVerificationForm()
    form.email.data = session['reset_email']  # Pre-fill email
    formclass = 'form-control'

    if form.validate_on_submit():
        email = session['reset_email']
        otp_code = form.otp_code.data
        
        success, message = verify_otp(email, otp_code)
        
        if success:
            # Generate secure token for password reset
            token = s.dumps(email, salt='verified-reset-salt')
            session['verified_reset_token'] = token
            flash("OTP verified successfully! You can now reset your password.", "success")
            return redirect(url_for('auth.reset_password_verified', token=token))
        else:
            flash(message, "danger")

    return render_template('verify_otp.html', form=form, formclass=formclass)

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    if 'reset_email' not in session:
        flash("Please start the password reset process again.", "warning")
        return redirect(url_for('auth.forgot_password'))
    
    email = session['reset_email']
    user = get_user_by_email(email)
    
    if user:
        # Generate and store new OTP
        otp_code = generate_otp()
        if store_otp(email, otp_code):
            # Send new OTP via email
            try:
                msg = Message("New Password Reset OTP - Employee Nexus", recipients=[email])
                msg.body = f"""Hi {user['first_name']},

Your new password reset OTP is: {otp_code}

This OTP is valid for 10 minutes and can be used only once.

If you didn't request this, please ignore this email.

Best regards,
Employee Nexus Team"""
                mail.send(msg)
                flash("New OTP has been sent to your email!", "success")
                
            except Exception as e:
                print("Mail Error:", e)
                flash("There was an issue sending the OTP. Try again later.", "danger")
        else:
            flash("Failed to generate OTP. Please try again.", "danger")
    else:
        flash("Email not found.", "danger")
    
    # Stay on the same OTP verification page
    return redirect(url_for('auth.verify_otp_route'))

@auth_bp.route('/reset-password-verified/<token>', methods=['GET', 'POST'])
def reset_password_verified(token):
    # Verify this is a verified token
    if session.get('verified_reset_token') != token:
        flash("Unauthorized access. Please complete OTP verification first.", "danger")
        return redirect(url_for('auth.forgot_password'))
    
    try:
        email = s.loads(token, salt='verified-reset-salt', max_age=600)  # 10 minutes
    except:
        flash("Reset session expired. Please start again.", "danger")
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    formclass = 'form-control'

    if request.method == 'POST':
        print("POST request received")  # Debug
        print(f"Form data: {request.form}")  # Debug
        print(f"Form validates: {form.validate()}")  # Debug
        print(f"Form errors: {form.errors}")  # Debug

    if form.validate_on_submit():
        print(f"Form validated successfully for email: {email}")  # Debug
        hashed_password = generate_password_hash(form.password.data)
        
        # Update password
        try:
            update_password(email, hashed_password)
            print("Password updated successfully")  # Debug
            
            # Clear session data
            session.pop('reset_email', None)
            session.pop('verified_reset_token', None)
            
            flash("Your password has been reset successfully!", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Error updating password: {e}")  # Debug
            flash("Error updating password. Please try again.", "danger")

    return render_template('reset_password.html', form=form, formclass=formclass)