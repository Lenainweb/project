from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jsglue import JSGlue
from flask_login import LoginManager
from config import basedir

app = Flask(__name__)
jsglue = JSGlue(app)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from app import views, models
