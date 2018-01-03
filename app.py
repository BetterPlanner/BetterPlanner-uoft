from flask import Flask, render_template, request
from pymongo import MongoClient
prereq = __import__('prerequisite')
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.test
collection = db.courses
prereq = db.prereq
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/search/', methods=["POST"])
def search_post():
    data = request.form["course"]
    courseInfo = collection.find_one({'course code':data})
    Prereq = prereq.find_one({data: {'$exists' : True}})
    return render_template("search.html",Data = courseInfo,prereqs = Prereq[data])


if __name__=='__main__':
    app.run(debug=True)