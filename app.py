import os
import firebase_admin
from firebase_admin import auth
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv 

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
    return '<h1>Hi!</h1>'

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
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
        orgs = list(collection.find())
        neworgs = []

        for names in orgs:
            name = names['name']
            location = names['location']
            shelf = {'name': name, 'location': location}
            neworgs.insert(0,shelf)

        return neworgs