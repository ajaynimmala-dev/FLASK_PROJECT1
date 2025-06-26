from flask import Flask,render_template,request,url_for,flash,redirect
from forms import RegistrationForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'e58ca8c71f5d9e5150acd9af436cc9f1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique = True,nullable = False)
    email = db.Column(db.String(50),unique = True,nullable = False)
    image_file = db.Column(db.String(20),unique = True,nullable = False,default = 'default.jpg')
    password = db.Column(db.String(60),nullable = False)
    posts = db.relationship('Post',backref='author',lazy = True)

    def __repr__(self):
        return f"User'{ self.username }','{self.email}','{self.image_file}'"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    date_posted = db.Column(db.DateTime,nullable= False,default = datetime.utcnow)
    content = db.Column(db.Text,nullable = False)
    userid = db.Column(db.Integer,db.Foreignkey('user.id'),nullable = False)
    def __repr__(self):
        return f"Post'{self.title}','{self.date_posted}'"


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
    print(form.validate_on_submit())
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('index'))
    else:
        return render_template('Register.html',title='Register',form=form)


@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        if form.email.data == 'ajay@gmail.com' and form.password.data == 'password':
            flash('You hava been logged in!','success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('Login.html',title='Login',form=form)


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)

