from appFuncs import login_mananger, userdb, bcrypt
from flask_login import UserMixin
import os
# This bit of code comes from the flask_login documentation
@login_mananger.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Each table in SQLAlchemy is defined as a class. Below is a table for user information.
class Admin(userdb.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = userdb.Column(userdb.Integer, primary_key=True)
    username = userdb.Column(userdb.String(20), unique=True, nullable=False)
    email = userdb.Column(userdb.String(120), unique=True, nullable=False)
    password = userdb.Column(userdb.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email})"

# Set a admin user that can login. To reset this, uncomment the before first request part in routes
def create_admin():
    username = os.environ.get('USERNAME')
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')
    admin = Admin(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    userdb.session.add(admin)
    userdb.session.commit()
    return