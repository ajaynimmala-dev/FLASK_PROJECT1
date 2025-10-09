from flask import Blueprint, current_app
from flask_login import current_user

from app.models import Post, LostFound
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename
from app import db
from app.posts.forms import LostItemForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/events")
def events():
    sample_events = [
        {
            "title": "Tech Fest 2025",
            "date": "2025-09-15",
            "location": "Auditorium, Main Campus",
            "description": "A full day of coding competitions, workshops, and project demos.",
            "image_file": "events/techfest.jpg"
        },
        {
            "title": "Sports Meet",
            "date": "2025-10-01",
            "location": "College Stadium",
            "description": "Annual sports meet with cricket, football, athletics and more.",
            "image_file": "events/sports.jpg"
        },
        {
            "title": "Cultural Night",
            "date": "2025-11-20",
            "location": "Open Air Theatre",
            "description": "Music, dance, drama and cultural performances by students.",
            "image_file": None  # No image, will show fallback
        }
    ]
    return render_template("events.html", events=sample_events)


@main.route("/announcements")
def announcements():
    sample_announcements = [
        {
            "title": "Semester Exams Notification",
            "date": "2025-09-20",
            "description": "Mid-semester exams will commence from October 10, 2025. Time-table will be released soon.",
            "image_file": "announcements/exam.jpg"
        },
        {
            "title": "Library Due Reminder",
            "date": "2025-09-18",
            "description": "Please return borrowed library books by September 25 to avoid late fees.",
            "image_file": None   # No image → fallback
        },
        {
            "title": "Holiday Notice",
            "date": "2025-10-02",
            "description": "College will remain closed on account of Gandhi Jayanti.",
            "image_file": "announcements/holiday.png"
        }
    ]
    return render_template("announcements.html", announcements=sample_announcements)

@main.route("/lost-and-found", methods=['GET', 'POST'])
def new_lost_item():
    form = LostItemForm()
    if form.validate_on_submit():
        filename = None
        if form.image_file.data:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(secure_filename(form.image_file.data.filename))
            filename = random_hex + f_ext
            filepath = os.path.join(current_app.root_path,"static/lost_found", filename)
            output_size = (600, 600)
            i = Image.open(form.image_file.data)
            i.thumbnail(output_size)
            i.save(filepath)
        new_item  = LostFound(title=form.title.data,
            location=form.location.data,
            description=form.description.data,
            contact=form.contact.data,
            image_file=filename,
            user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        flash(f"Lost item '{form.title.data}' has been reported!", "success")
        return redirect(url_for('main.home'))

    return render_template("lost_and_found.html", form=form)


