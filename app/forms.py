from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])

    email=StringField('Email',validators=[DataRequired(),Email()])

    password=PasswordField('Password',validators=[DataRequired()])

    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])

    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is already exists!')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is already exists!')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])

    password=PasswordField('password',validators=[DataRequired()])

    remember=BooleanField('Saved password')

    submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired(),Length(min=2,max=20)])

    email = StringField('Email',validators = [DataRequired(),Email()])

    picture = FileField('Update Profile Picture',validators = [FileAllowed(['jpg','png','jpeg'])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is already exists!')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is already exists!')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('submit')