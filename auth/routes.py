from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message

from .forms import LoginForm, ForgotPasswordForm, ResetPasswordForm
from ..models.employee import get_user_by_email, update_password
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
            token = s.dumps(email, salt='reset-password-salt')
            link = url_for('auth.reset_with_token', token=token, _external=True)

            # Send email
            try:
                msg = Message("Password Reset Request", recipients=[email])
                msg.body = f"Hi {user['first_name']},\n\nClick the link below to reset your password:\n{link}\n\nThis link will expire in 15 minutes."
                mail.send(msg)
                flash("A password reset link has been sent to your email.", "success")
            except Exception as e:
                print("Mail Error:", e)
                flash("There was an issue sending the email. Try again later.", "danger")

            return redirect(url_for('auth.login'))
        else:
            flash("Email ID not found.", "danger")
            return redirect(url_for('auth.forgot_password'))

    return render_template('forgot_password.html', form=form, formclass=formclass)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    form = ResetPasswordForm()
    formclass = 'form-control'

    try:
        email = s.loads(token, salt='reset-password-salt', max_age=900)  # 15 minutes validity
    except:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        update_password(email, hashed_password)
        flash("Your password has been reset successfully!", "success")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form, formclass=formclass)