from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp, EqualTo, ValidationError

class EmployeeRegistrationForm(FlaskForm):
    salutation = SelectField('Salutation:',
                           choices=[('','Select'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], 
                           validators=[DataRequired(message="Please select a salutation.")])
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
    create_password = PasswordField('Create Password:', validators=[
        DataRequired(), 
        Length(min=8, message="Password must be at least 8 characters"),
        Regexp(r'^(?=.*[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?])', message="Password must contain at least one special character."),
        Regexp(r'^(?=.*[A-Z])', message="Password must contain at least one uppercase letter"),
        Regexp(r'^(?=.*[a-z])', message="Password must contain at least one lowercase letter")
    ])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('create_password', message='Passwords must match')])
    submit = SubmitField('Submit')
