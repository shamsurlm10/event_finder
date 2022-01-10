import os

from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flaskr import users

load_dotenv()

# Create and Configure the App
app = Flask(__name__)

# Secret Keys
app.secret_key = os.getenv("SECRET_KEY")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/images/uploads"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")


# Database
db = SQLAlchemy(app)

# Marshmallow
ma = Marshmallow(app)

# Migration
migrate = Migrate(app, db)

# Encryption
bcrypt = Bcrypt(app)

# Login-Manager
login_manager = LoginManager(app)

login_manager.login_view = "users.login_user"
login_manager.login_message_category = "primary"


# Mail
mail = Mail(app)


import flaskr.models

from flaskr.admins.routes import admins
from flaskr.api.comment import comments
from flaskr.api.post import posts
from flaskr.api.reply import replies
from flaskr.events.routes import events
from flaskr.mains.routes import mains
from flaskr.notifications.routes import notifications
from flaskr.profiles.routes import profiles
from flaskr.users.routes import users

# Registering blueprints
app.register_blueprint(users)
app.register_blueprint(profiles)
app.register_blueprint(mains)
app.register_blueprint(admins)
app.register_blueprint(events)
app.register_blueprint(notifications)
app.register_blueprint(posts)
app.register_blueprint(comments)
app.register_blueprint(replies)
