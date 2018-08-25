from flask import Flask, render_template, request
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.test
test_db        = client.test
utm_course     = test_db.utm_courses
utsc_course    = test_db.utsc_courses
utsg_course    = test_db.utsg_courses

@app.route('/')
def INDEX():
    return render_template("index.html")

@app.route('/search', methods=["POST", "GET"])
def search_post():
    data = request.args.get('course').upper()

    info =[]
    utscData = utsc_course.find().batch_size(500)
    utmData = utm_course.find().batch_size(500)
    utsgData = utsg_course.find().batch_size(500)

    if data[3].isalpha():
        data = data[:3] + chr(ord(data[3])-16) + data[4:]

    for i in utsgData:
        if i.get('code')==data:
            info.append(i)
            break
        if i.get('code')==data+"H1":
            info.append(i)
            break
        if i.get('code')==data+"Y1":
            info.append(i)
            break

    for k in utmData:
        if k.get('code')==data:
            info.append(k)
            break
        if k.get('code')==data+"H5":
            info.append(k)
            break
        if k.get('code')==data+"Y5":
            info.append(k)
            break

    if not data[3].isalpha():
        data = data[:3] + chr(ord(data[3])+16) + data[4:]

    for j in utscData:
        if j.get('code')==data:
            info.append(j)
            break
        if j.get('code')==data+"H3":
            info.append(j)
            break
        if j.get('code')==data+"Y3":
            info.append(j)
            break


    if info:
        if len(info)>1:
            return render_template("search_result.html", Data=info)
        else:
            url = url_for_campus(info[0]['campus'],info[0]['division'],info[0]['code'])
            return render_template("search_new.html", Data=info[0], url=url)
    else:
        return render_template("/index.html")

def url_for_campus(campus,division,course):
    url=""
    if campus == "UTM":
        url="https://student.utm.utoronto.ca/calendar/OpenCourse.pl?Course="+course
    elif campus == "UTSC":
        url = "https://utsc.calendar.utoronto.ca/course/"+course
    elif campus == "UTSG":
        if division == "Faculty of Arts and Science":
            url = "https://fas.calendar.utoronto.ca/course/"+course
        elif division == "Faculty of Applied Science & Engineering":
            url = "https://portal.engineering.utoronto.ca/sites/calendars/current/Course_Descriptions.html#"+course
        elif division == "John H. Daniels Faculty of Architecture, Landscape, & Design":
            url = "https://daniels.calendar.utoronto.ca/course/"+course
        else:
            url = "https://www.utoronto.ca/"
    else:
        url = "https://www.utoronto.ca/"
    return url

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
