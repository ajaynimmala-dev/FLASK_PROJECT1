from flask import render_template,url_for,flash,redirect,request
from app.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from app import app,db,bcrypt
from app.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets,os
from PIL import Image


@app.route('/',methods=['GET','POST'])
def index():
    posts = Post.query.all()6=
    return render_template('home.html',posts=posts,title='website design')


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



@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember = form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check email and password','danger')
                return redirect(url_for('login'))
        else:
            return render_template('Login.html',title='Login',form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file, form=form)



@app.route("/post/new",methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('index'))
    else:
        return render_template('create_post.html',title = 'New Post',form = form)