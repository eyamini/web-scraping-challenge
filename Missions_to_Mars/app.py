from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Establish PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route  to index template Mongo data
@app.route("/")
def index():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_info)

# Initiate Scraper
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
