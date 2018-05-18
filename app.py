from flask import Flask, render_template, request
from pymongo import MongoClient
#from webScraper import HTMLParser
#from prerequisite import recognized_prereq
#web = __import__('webScraper')

#rec_prereq = __import__('prerequisite')
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.test
collection = db.courses
prereq = db.prereq

@app.route('/')
def INDEX():
    return betteruoft()

@app.route('/better-uoft/')
def betteruoft():
    return render_template("index.html")

@app.route('/better-uoft/search/', methods=["POST"])
def search_post():
    data = request.form["course"].upper()
    info=""
    courseData = collection.find().batch_size(300)#.find_one({'course code':data})
    for i in courseData:
        if i.get('course code')==data:
            info = i
            break;
        if i.get('course code')==data+"H5":
            info = i
            data = data+"H5"
            break;
        if i.get('course code')==data+"Y5":
            info = i
            data = data+"Y5"
            break;


    Prereq = prereq.find_one({data: {'$exists' : True}})
    if info:
        if Prereq:
            return render_template("search.html",Data = info,prereqs = Prereq[data])
        else:
            return render_template("search.html",Data = info)
    else:
        return render_template("/index.html")

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
