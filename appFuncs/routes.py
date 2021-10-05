import base64
import json
from ast import literal_eval
from appFuncs import app, sql, con, dictionary_convertion, plot, config_data, bcrypt, userdb
from flask import render_template, request, current_app, redirect, url_for, flash
from appFuncs.models import Admin, create_admin
from appFuncs.forms import login_form, registration_form, heliostat_select
from flask_login import login_user, current_user, logout_user, login_required


MESSAGES = []
NUM = 0

# TODO: Check the config function again. see below

# @app.before_first_request
# def init():
#     create_admin()
#     return 'OK', 200

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = login_form()
    if form.validate_on_submit():
       user = Admin.query.filter_by(email=form.email.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember.data)
           next_page = request.args.get('next')
           return redirect(next_page) if next_page else redirect(url_for('home'))
       else:
            flash('Login not successful. Please check email and password', 'danger')

    return render_template('login.html', title=login, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        dictionary_data = []
        helio_list = sql.selectall(con=con, tname='helio_list', cols='helio_id', pattern='order by helio_id asc')
        for helio_id in helio_list:
            helio = helio_id.split(".", 1)
            helio = ''.join(helio)
            row_id = sql.selectall(con=con, tname=f'helio{helio}', cols='id')  # list of id's
            i = 0

            for num in row_id:
                row_id[i] = int(num)
                i += 1

            largest_id = max(row_id)
            cols = ['helio_id', 'date', 'status']
            helio_data = sql.select(con=con, tname=f'helio{helio}',
                                    cols=cols, pattern=f'id={largest_id}')  # helio_data is a list of key/value pairs
            helio_dict = dictionary_convertion.data_dict(helio_data, cols)
            dictionary_data.append(helio_dict)
        return render_template('home.html', messages=dictionary_data)
    return 'OK', 200

# This endpoint receives all the pubsub messages and appends them o the global messages list
# TODO: make this function a cloud function rather with the SQL database as its memory
@app.route('/pubsub/push', methods=['POST'])
@login_required
def pubsub_push():
    # Check validation token
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    # If token is accepted, retrieve data
    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])

    MESSAGES.append(payload.decode('utf-8'))
    # TODO: Check this function again as well as the limiting function
    length = len(MESSAGES)
    global NUM
    num = NUM
    while length > num:
        i = num
        try:
            msg = literal_eval(MESSAGES[i])
            config_data.config_test(msg)
        except:
            return ' NOT OK', 200
        num = num + 1
        NUM = num
    # Returning any 2xx status indicates successful receipt of the message.
    return 'OK', 200

# This route has Google Data Studio's report embedded but only people with the link can see the graph so access must
# be assigned for that in Google Data Studio
@app.route('/data_report')
@login_required
def embedded_graph():
    return render_template('graph.html', title='Data Graph')

@app.route('/choose_helio', methods=['GET', 'POST'])
@login_required
def choose_helio():
    form = heliostat_select()
    if form.is_submitted():
        helio_num = form.heliostat.data
        return redirect(url_for('matplot_graph', helio_id=helio_num))
    return render_template('choose_helio.html', title='Choose heliostat', form=form)

@app.route('/helio_graph<helio_id>', methods=['GET', 'POST'])
def matplot_graph(helio_id):
    if helio_id is not None:
        bat, m1, m2 = plot.plot(helio_id)
        return render_template('custom_graphs.html', bat=bat, m1=m1, m2=m2, helio_id=helio_id, title='information graphs')
    return redirect(url_for('choose_helio'))

# @app.route('/registration', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = registration_form()
#     if form.validate_on_submit():
#         # Database structure defined in models.py
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash password
#         user = Admin(username=form.username.data, email=form.email.data, password=hashed_password)  # Create user
#         userdb.session.add(user)  # Add user to database stack
#         userdb.session.commit()   # Submit stack to database
#         flash('Your account has been created, you can now login', 'success')
#         return redirect(url_for("login"))
#     return render_template('register.html', title='Registeration', form=form)