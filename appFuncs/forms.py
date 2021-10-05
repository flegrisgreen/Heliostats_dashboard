from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from appFuncs.models import Admin
from appFuncs import sql, con

class login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class registration_form(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # These functions are custom validator functions that check that the username and email are unique
    def validate_username(self, username):
        user = Admin.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is not unique, please choose a different one')

    def validate_email(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is not unique, please choose a different one')


def list_choices():
    choices = []
    helio_list = sql.selectall(con=con, tname='helio_list', cols='helio_id', pattern='order by helio_id asc')
    for helio in helio_list:
        choice = (helio, helio)
        choices.append(choice)
    return choices

class heliostat_select(FlaskForm):

    choices = list_choices()
    heliostat = SelectField('Select a heliostat', choices=choices)
    submit = SubmitField('Plot heliostat data')