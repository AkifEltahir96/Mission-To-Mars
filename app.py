# Importing Dependencies

# Use flask to render a template, redirect to another url and create a url
from flask import Flask, render_template, redirect, url_for
# Use PyMongo to interact with out Mongo database
from flask_pymongo import PyMongo 
# Use the scraping file we converted from Jupyter Notebook to Python
import scraping

# Setting up Flask

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Line 15 tells us that python that our app will connect to Mongo using a URI.
    # URI is a uniform resource identifier similar to URL
# "mongodb://localhost:27017/mars_app" is the URI we will use to connect our app to Mongo.
    # We will reach Mongo through our localhost server, using port 27017 through the database mars_app

@app.route("/")
def index():
   mars = mongo.db.mars.find_one() # locates the mars collection
   return render_template("index.html", mars=mars) # returns an 
