import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or  'dev_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ajaykumarnimmala18@gmail.com'
    MAIL_PASSWORD = 'hrwmusceilshcxqr'