import bson 
import os
from dotenv import load_dotenv 
from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
# access your MongoDB Atlas cluster
load_dotenv()
connection_string = os.environ.get('CONNECTION_STRING')
mongo_client: MongoClient = MongoClient(connection_string)

# add in your database and collection from Atlas 
database: Database = mongo_client.get_database('orgs')
collection: Collection = database.get_collection('orgs')

# orgs = {'name': 'org3', 'location': 'location3'}
# collection.insert_one(orgs)

# instantiating new object with “name”
app: Flask = Flask(__name__)

# our initial form page
@app.route("/")
def index():
	return 'Hi!'

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