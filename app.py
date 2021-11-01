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

@app.route("/") # tells Flask what to display when we're looking at the home page
def index():
   mars = mongo.db.mars.find_one() # locates the mars collection
   return render_template("index.html", mars=mars) # returns an HTML template using an index.HTML file.

@app.route("/scrape") # this route will run the function scrape
def scrape():
   mars = mongo.db.mars # references the Mongo database
   mars_data = scraping.scrape_all() # holds all of the scraping data in the scraping.py file
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302) # redirect to the / page where we can see updated content.

   # Line 32 tells us we will update the database. 
    # We need an empty dictionary (JSON object) to add data into the db
    # We are collecting the data from mars_data
    # upsert=True indicated to create a new document in Mongosh

if __name__ == '__main__':
    app.run()


