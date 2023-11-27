import os
import firebase_admin
from firebase_admin import auth
from flask import Flask, request, render_template, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv 
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask import Markup
from flask import session
from flask import redirect, url_for

# Initialize the Firebase Admin SDK
cred = firebase_admin.credentials.Certificate('testmongo.json')
firebase_admin.initialize_app(cred)

# access your MongoDB Atlas cluster
load_dotenv()
connection_string = os.environ.get('CONNECTION_STRING')
mongo_client: MongoClient = MongoClient(connection_string)

# add in your database and collection from Atlas 
database: Database = mongo_client.get_database('Neuro')
collection: Collection = database.get_collection('assessment')

# instantiating new object with “name”
app: Flask = Flask(__name__)

# @app.route('/verify_id_token', methods=['POST'])
# def verify_id_token():
#     request_data = request.get_json()
#     print(request_data)
#     if request_data is None or 'idToken' not in request_data:
#         return 'Bad request', 400
#     id_token = request_data['idToken']

# our initial form page
@app.route("/")
def index():
    first_name = "John"

app.config['SECRET_KEY'] = "mysecretkey"



class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    
@app.before_request
def before_request():
    if 'user' in session and request.endpoint in ['signin', 'signup']:
        return redirect(url_for('user', name=session['user']))
    
# for debugging purposes   
@app.route('/check_user', methods=['GET'])
def check_user():
    if 'user' in session:
        return f"User {session['user']} is currently signed in."
    else:
        return "No user is currently signed in."


@app.route('/api/signin', methods=['POST'])
def api_signin():
    email = request.json.get('email')
    if email:
        session['user'] = email
        return jsonify({'message': 'User signed in successfully'}), 200
    else:
        return jsonify({'message': 'No email provided'}), 400
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if the user is already registered
        try:
            user = auth.get_user_by_email(email)
            flash(Markup("<strong>Holy guacamole!</strong> You're already registered. Please <a href='signin.html' class='alert-link'>sign in</a>."), 'error')
            return render_template('signup.html', title='Sign Up', form=form)
        except auth.UserNotFoundError:
            # User does not exist, check if the passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('signup.html', title='Sign Up', form=form)

            # Create a new user
            user = auth.create_user(
                email=email,
                password=password
            )
            flash('User {0} created successfully'.format(user.uid), 'success')

    return render_template('signup.html', title='Sign Up', form=form)



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = auth.get_user_by_email(email)

        except auth.UserNotFoundError:
            # If the user does not exist, flash an error message
            flash('User does not exist', 'error')
    return render_template('signin.html', title='Sign In', form=form)



@app.route('/user')
def user():
    return render_template('user.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/orgs', methods=['GET'])
def get_orgs():
    orgs = list(collection.find())  # Retrieve all documents
    for org in orgs:  # Convert ObjectIds to strings
        org['_id'] = str(org['_id'])
    return jsonify(orgs)  # Convert list to JSON and return it


# CREATE and READ 
@app.route('/usrs', methods=["GET", "POST"])
def usrs():
    if request.method == 'POST':
        # CREATE
        name: str = request.json['name']
        location: str = request.json['location']

        # insert new book into books collection in MongoDB
        collection.insert_one({"name": name, "location": location})

        return f"CREATE: Your orgs {name} ({location} location) has been added.\n "

    elif request.method == 'GET':
        # READ
        neuro = list(collection.find())
        neworgs = []

        for names in orgs:
            name = names['name']
            location = names['location']
            shelf = {'name': name, 'location': location}
            neworgs.insert(0,shelf)

        return neworgs