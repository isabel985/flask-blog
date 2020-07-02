import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Database addresses are constructed as protocol;://dbname:password@domain:port/username

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'database.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
  FLASK_APP = os.getenv('FLASK_APP')
  FLASK_ENV = os.getenv('FLASK_ENV')
  MAIL_SERVER = os.getenv('MAIL_SERVER')
  MAIL_PORT = os.getenv('MAIL_PORT')
  MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
  MAIL_USERNAME = os.getenv('MAIL_USERNAME')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
  ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
