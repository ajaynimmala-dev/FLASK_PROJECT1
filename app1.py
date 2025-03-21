from flask import Flask,render_template,request,url_for

from forms import RegistrationForm,LoginForm
app=Flask(__name__)

app.config['SECRET_KEY']='e58ca8c71f5d9e5150acd9af436cc9f1'

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
@app.route('/')
def home():
    return render_template('home.html',posts=data,title='website design')

@app.route('/about')
def about():
    return render_template('about.html',title='abcd')


@app.route('/get',methods=['POST','GET'])
def getData():
    temp=request.form
    return 'success'

@app.route('/register',methods=['POST','GET'])
def register():
    form=RegistrationForm()
    return render_template('Register.html',title='Register',form=form)

@app.route('/login')
def login():
    form=LoginForm()
    return render_template('Login.html',title='Login',form=form)

if __name__=='__main__':
    app.run(debug=True)

