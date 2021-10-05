import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from google.cloud import pubsub_v1
from appFuncs.sql_interface import sql_interface

sql = sql_interface()
con = sql.open_connection()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
userdb = SQLAlchemy()  #Local database instance for user login information
userdb.init_app(app)

app.secret_key = os.environ['SECRET_KEY']  # Generated using token_hex() from secrets module. This secures cookies
bcrypt = Bcrypt(app)

login_mananger = LoginManager(app)
login_mananger.login_view = 'login'  # This redirects the user to the login page if they manually try to access the account page
login_mananger.login_message_category = 'info'  # Change font and style of alert message

# App.config variable declarations
app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
app.config['PROJECT'] = os.environ['PROJECT']

client = pubsub_v1.PublisherClient()

from appFuncs import routes