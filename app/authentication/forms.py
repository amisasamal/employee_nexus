from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

class LoginForm(FlaskForm):
    email = StringField('Email ID:', validators=[DataRequired(), Email(), Length(max=32)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email ID:', validators=[DataRequired()])
    submit = SubmitField('Next')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password:', validators=[
        DataRequired(), 
        Length(min=8, message="Password must be at least 8 characters"),
        Regexp(r'^(?=.*[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?])', message="Password must contain at least one special character."),
        Regexp(r'^(?=.*[A-Z])', message="Password must contain at least one uppercase letter"),
        Regexp(r'^(?=.*[a-z])', message="Password must contain at least one lowercase letter")
    ])
    confirm_password = PasswordField('Confirm Password:', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')