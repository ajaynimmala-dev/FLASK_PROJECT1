from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'e58ca8c71f5d9e5150acd9af436cc9f1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from app import routes