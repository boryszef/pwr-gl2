from flask import Flask
from flask_login import LoginManager
from flask_menu import Menu
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import configparser
import os
from app.views import main


def prepare_env():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read('config.ini')
    for key in config['global']:
        val = config['global'][key]
        os.environ[key] = val


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(main)
login = LoginManager(app)
Menu(app=app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#db.create_all()

prepare_env()
#from app.model import User