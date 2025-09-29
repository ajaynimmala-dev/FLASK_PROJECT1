from flask import Blueprint, current_app
from flask_login import login_required

from app.models import Post
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename
from app import db
from app.posts.forms import LostItemForm

main = Blueprint('main', __name__)

training_schedule = [
    {
        'number': 1,
        'title': 'Fire Safety',
        'videos': [
            {'title': 'Fire Extinguisher Basics', 'link': 'https://youtu.be/yodLMfOZNvA?si=vPgKTRuhiTw0VyZq'},
            {'title': 'Evacuation Drill Demo', 'link': 'https://youtu.be/3aLWlDY_G9w?si=k5pN4XrfHniHY0K7'}
        ],
        'quiz_link': '/quiz/week1'
    },
    {
        'number': 2,
        'title': 'Earthquake Preparedness',
        'videos': [
            {'title': 'Drop, Cover, Hold', 'link': 'https://youtu.be/BLEPakj1YTY?si=OG11GMl3eLArHqx7'},
            {'title': 'Earthquake Safety Checklist', 'link': 'https://youtu.be/hWSu4l1RxLg?si=PbdZn4_roOI2-L8i'}
        ],
        'quiz_link': '/quiz/week2'
    },
    {
        'number': 3,
        'title': 'Flood Safety',
        'videos': [
            {'title': 'Preparing for Floods', 'link': 'https://youtu.be/43M5mZuzHF8?si=SAHbMP817onWbeaf'},
            {'title': 'Evacuation Routes', 'link': 'https://youtu.be/3E4z-mEAPoo?si=KyxGy2ZOw21-qy4I'}
        ],
        'quiz_link': '/quiz/week3'
    }
]

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/incidents")
def show_incidents():
    # Dummy incident data (no database)
    incidents = [
    {
        "title": "Earthquake Tremors Felt",
        "location": "Delhi - Connaught Place",
        "description": "Mild tremors were reported at 7:30 AM. No damage reported so far.",
        "contact": "Delhi Disaster Helpline - 1077",
        "image": "https://via.placeholder.com/400x200"
    },
    {
        "title": "Flooding in Residential Area",
        "location": "Mumbai - Andheri East",
        "description": "Heavy rains caused waterlogging in several parts of the city.",
        "contact": "Mumbai Municipal Helpline - 1916",
        "image": "https://via.placeholder.com/400x200"
    },
    {
        "title": "Fire at College Campus",
        "location": "Chennai - Anna Nagar",
        "description": "A small fire broke out in the library building. Fire services controlled the situation.",
        "contact": "Chennai Fire Dept - 101",
        "image": "https://via.placeholder.com/400x200"
    }]
    return render_template("incidents.html", incidents=incidents)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/training")
def training():
    return render_template('training.html', title='Training',training_schedule=training_schedule)

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

        flash(f"Lost item '{form.title.data}' has been reported!", "success")
        return redirect(url_for('main.home'))

    return render_template("lost_and_found.html", form=form)


@main.route("/my_progress")
@login_required
def my_progress():
    student_progress = {
        "name": "Aarav Sharma",
        "student_class": "10th Grade",
        "attendance": 92,
        "exam_score": 85,
        "training_completion": 70,
        "points": 120,
        "level": 3,
        "coins": 250,
        "badges": [
            {"name": "Fire Safety Expert", "earned": True},
            {"name": "Flood Awareness Champion", "earned": False},
        ],
        "status": "On Track",  # Status text
        "status_color": "success",  # Bootstrap badge color: success, warning, danger
        "profile_pic": "profile_pics/student1.jpg"
    }
    return render_template("progress.html",student=student_progress)

@main.route("/leaderboard")
def leaderboard():
    students = [
        {
            "name": "Aarav Sharma",
            "student_class": "10th Grade",
            "score": 95,
            "attendance": 92,
            "training_completion": 80,
            "rank": 1,
            "rank_color": "success",   # green badge
            "profile_pic": "profile_pics/student1.jpg"
        },
        {
            "name": "Sneha Patel",
            "student_class": "9th Grade",
            "score": 88,
            "attendance": 85,
            "training_completion": 70,
            "rank": 2,
            "rank_color": "primary",   # blue badge
            "profile_pic": "profile_pics/student2.jpg"
        },
        {
            "name": "Rohan Verma",
            "student_class": "11th Grade",
            "score": 80,
            "attendance": 78,
            "training_completion": 60,
            "rank": 3,
            "rank_color": "warning",   # yellow badge
            "profile_pic": None
        }
    ]
    return render_template("leaderboard.html", students=students)

from flask import render_template
from datetime import datetime

@main.route("/weather")
@login_required
def weather():
    # Example dummy data
    forecast = {
        "city": "Guntur",
        "date": datetime.now().strftime("%d %b %Y"),
        "temperature": "34°C",
        "condition": "Sunny",
        "disaster_risk": "Low flood risk",
        "alerts": ["High UV Index", "Air Quality Moderate"]
    }
    return render_template("weather.html", forecast=forecast)

from flask import render_template
from flask_login import login_required
from datetime import datetime

@main.route("/alerts")
@login_required
def alerts():
    # Dummy emergency alerts
    emergency_alerts = [
        {
            "title": "Cyclone Warning",
            "description": "Cyclone expected in the coastal areas tomorrow. Stay indoors and follow safety instructions.",
            "date": datetime.now().strftime("%d %b %Y %H:%M"),
            "severity": "High"
        },
        {
            "title": "Flood Alert",
            "description": "Heavy rains expected in Delhi-NCR. Avoid low-lying areas and follow evacuation protocols.",
            "date": datetime.now().strftime("%d %b %Y %H:%M"),
            "severity": "Moderate"
        },
        {
            "title": "Heatwave Advisory",
            "description": "Temperature may rise above 45°C. Stay hydrated and avoid outdoor activities during peak hours.",
            "date": datetime.now().strftime("%d %b %Y %H:%M"),
            "severity": "Low"
        }
    ]
    return render_template("alerts.html", alerts=emergency_alerts)
