from flask import render_template,url_for,flash,redirect
from app.forms import RegistrationForm,LoginForm
from app import app,db,bcrypt
from app.models import User,Post
from flask_login import login_user,current_user,logout_user

data=[{
    'author':'Corey Schafer',
    'title':'Blog Post 1',
    'content':'First post content',
    'date_posted':'April 20,2018'
},{
    'author':'Jane Doe',
    'title':'Blog Post 2',
    'content':'Second post content',
    'date_posted':'April 21,2018'
}]

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('home.html',posts=data,title='website design')


@app.route('/about')
def about():
    return render_template('about.html',title='abcd')


@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form=RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username = form.username.data,email = form.email.data,password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You may able to login','success')
            return redirect(url_for('login'))
        else:
            return render_template('Register.html',title='Register',form=form)


@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember = form.remember.data)
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check email and password','danger')
                return redirect(url_for('login'))
        else:
            return render_template('Login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
