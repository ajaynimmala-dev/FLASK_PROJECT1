from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=40)])

    register_number = StringField('RegisterNumber', validators=[DataRequired(), Length(min = 8,max = 8)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    available_departments = [("CS", "CSE"), ("DS", "DataScience"),("AIML","Artificial Intelligence and MachineLearning"),("MEC","Mechanical"),("Civ","Civil"),("CSBS","Business Systems"),("Iot","Internet of Things"),("Ece","Electronics and communications Engineering"),("EEE","Electrical and Electronics Engineering")]

    department = SelectField("Department", validators=[DataRequired()], choices=available_departments)

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('password', validators=[DataRequired()])

    remember = BooleanField('Saved password')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=40)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already exists!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already exists!')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('ResetPassword', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')
