import bson 
import os
from dotenv import load_dotenv 
from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
# access your MongoDB Atlas cluster
load_dotenv()
connection_string: str = os.environ.get('CONNECTION_STRING')
mongo_client: MongoClient = MongoClient(connection_string)

# add in your database and collection from Atlas 
database: Database = mongo_client.get_database('bookshelf')
collection: Collection = database.get_collection('books')

book = {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'year': 1925}
collection.insert_one(book)
# instantiating new object with “name”
app: Flask = Flask(__name__)

# our initial form page
@app.route("/")
def index():
	return 'Hi!'


app: Flask = Flask(__name__)
# our initial form page 
@app.route("/") 
def index():
	return 'Hi!'