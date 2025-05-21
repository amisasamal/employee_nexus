from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp, EqualTo
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os

import app_db

#---------------------- REGISTRATION FORM ----------------------------
class Simpleform(FlaskForm):
    salutation = SelectField('Salutation:',choices=[('','Select'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], validators=[DataRequired(message="Please select a salutation.")])
    def validate_salutation(form, field):
        if field.data == '':
            raise ValidationError('Please select a salutation.')
    first_name = StringField('First Name:', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name:', validators=[Length(max=40)])
    last_name = StringField('Last Name:', validators=[DataRequired(), Length(max=40)])
    date_of_birth = DateField('Date of Birth:', format='%Y-%m-%d', validators=[DataRequired()])
    joined_on = DateField('Joined On:', format='%Y-%m-%d', validators=[DataRequired()])
    post = StringField('Post:', validators=[DataRequired(), Length(max=100)])
    mobile_number = StringField('Mobile Number:', validators=[DataRequired(), Regexp(r'^[6-9]\d{9}$', message="Enter a valid 10-digit mobile number.")])
    email_id = StringField('Email ID:', validators=[DataRequired(), Email(message='Please Input Valid Email')])
    create_password = PasswordField('Create Password:', validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters"),
                        Regexp(r'^(?=.*[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?])', message="Password must contain at least one special character."),
                        Regexp(r'^(?=.*[A-Z])', message="Password must contain at least one uppercase letter"),
                        Regexp(r'^(?=.*[a-z])', message="Password must contain at least one lowercase letter")])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('create_password', message='Passwords must match')])
    submit = SubmitField('Submit')

#---------------------LOGIN FORM---------------------------
class LoginForm(FlaskForm):
    email = StringField('Email ID:', validators=[DataRequired(), Email(), Length(max=32)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email ID:', validators=[DataRequired()])
    submit = SubmitField('Next')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')


app=Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# Email Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your provider's SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Consider using an app password(not your gmail password)
app.config['MAIL_DEFAULT_SENDER'] = 'amisasamal3@gmail.com'

mail = Mail(app)
# Token Serializer
s = URLSafeTimedSerializer(app.secret_key)

def generate_employee_id():
    return uuid.uuid4().hex[:8]  # 8-character unique string

#----------------REGISTRATION---------------------

@app.route('/')
def index():
    form=Simpleform()
    formclass = 'form-control'
    
    return render_template('index.html',form=form,formclass=formclass)

@app.route('/submit', methods=['POST'])
def submit():
    form=Simpleform()
    formclass = 'form-control'

    if form.validate_on_submit():
       emp_info={
            'employee_id':generate_employee_id(),
            'salutation':form.salutation.data.strip(),
            'first_name':form.first_name.data.strip(),
            'middle_name':form.middle_name.data.strip(),
            'last_name':form.last_name.data.strip(),
            'date_of_birth':form.date_of_birth.data,
            'joined_on':form.joined_on.data,
            'post':form.post.data.strip(),
            'mobile_number':form.mobile_number.data.strip(),
            'email_id':form.email_id.data.strip(),
            'password':generate_password_hash(form.confirm_password.data.strip())
       }
       print('emp_info',emp_info)   
       existing_user = app_db.get_user_by_email(emp_info['email_id'])
       if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('index'))

       try:
            app_db.submit_data(emp_info) 
            flash(f"You have successfully submitted your data {emp_info['salutation']} {emp_info['first_name']}")
            return render_template('registered.html')
       except Exception as e:
            flash(f"An error occurred while saving your data. Please try again later.", "danger")
            print("Database Error:", e)  # Log the actual error in console for debugging
            return redirect(url_for('index'))

    else:
        flash("There are errors in the form. Please fix them and submit again.", "danger")
        print('error',form.errors)
        return render_template('index.html',form=form,formclass=formclass)  
    
#-----------------LOGIN----------------------

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    formclass = 'form-control'

    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
         # Fetch user data from DB
        user = app_db.get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            # flash('Login Successful!', 'success')

            # Store user info in session (or just ID/email)
            session['user'] = {
                'email': user['email_id'],
                'employee_id': user['employee_id']
            }

            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form, formclass=formclass)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    email = session['user']['email']

    # Fetch full user info from DB
    user = app_db.get_user_by_email(email)

    return render_template('dashboard.html', user=user)


@app.route('/logout', methods=['POST'])
def logout():
    print(session['user'])
    session.clear()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    formclass = 'form-control'

    if form.validate_on_submit():
        email = form.email.data.strip()
        user = app_db.get_user_by_email(email)

        if user:
            token = s.dumps(email, salt='reset-password-salt')
            link = url_for('reset_with_token', token=token, _external=True)

            # Send email
            try:
                msg = Message("Password Reset Request", recipients=[email])
                msg.body = f"Hi {user['first_name']},\n\nClick the link below to reset your password:\n{link}\n\nThis link will expire in 15 minutes."
                mail.send(msg)
                flash("A password reset link has been sent to your email.", "success")
            except Exception as e:
                print("Mail Error:", e)
                flash("There was an issue sending the email. Try again later.", "danger")

            return redirect(url_for('login'))
        else:
            flash("Email ID not found.", "danger")
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html', form=form, formclass=formclass)



@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    form = ResetPasswordForm()
    formclass = 'form-control'

    try:
        email = s.loads(token, salt='reset-password-salt', max_age=900)  # 15 minutes validity
    except SignatureExpired:
        flash("The reset link has expired.", "danger")
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash("Invalid or tampered reset link.", "danger")
        return redirect(url_for('forgot_password'))

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        app_db.update_password(email, hashed_password)
        flash("Your password has been reset successfully!", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form, formclass=formclass)



#----------------------------------------------------------------------------------------------------------------------------------
# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
#----------------------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    app.run(debug=True)    