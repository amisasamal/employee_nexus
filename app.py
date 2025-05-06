from flask import Flask,render_template,request,flash,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp, EqualTo
import random
from werkzeug.security import generate_password_hash

import app_db

class Simpleform(FlaskForm):
    salutation = SelectField('Salutation:',choices=[('','Select'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], validators=[DataRequired()])
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

app=Flask(__name__)
app.secret_key = 'sdrw35747o8[-0]ygfasa'

def generate_id():
    return random.randint(10000000, 99999999)

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
            'employee_id':generate_id(),
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
       # return redirect(url_for('index'))

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
    
if __name__=='__main__':
    app.run(debug=True)    