from flask import render_template,url_for,flash,redirect
from app.forms import RegistrationForm,LoginForm
from app import app
from app.models import User,Post

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
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('index'))
    else:
        return render_template('Register.html',title='Register',form=form)


@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'ajay@gmail.com' and form.password.data == 'password':
            flash('You hava been logged in!','success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('Login.html',title='Login',form=form)
