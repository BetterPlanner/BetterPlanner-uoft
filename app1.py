from flask import Flask, render_template, request
from pymongo import MongoClient
#from webScraper import HTMLParser
#from prerequisite import recognized_prereq
#web = __import__('webScraper')

#rec_prereq = __import__('prerequisite')
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.test
test_db        = client.test
utm_course     = test_db.utm_courses
utsc_course    = test_db.utsc_courses
utsg_course    = test_db.utsg_courses
# prereq         = test_db.prereq


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
    # utsc_code=""
    # utsg_code=""
    # utm_code=""
    #
    # if len(data) == 6:
    #
    #     utsg_code = data+"H1"
    #     utsc_code = data+"H3"
    #     utm_code = data+"H5"
    #
    #     utsgcourse = utsg_course.find({"code":utsg_code})
    #     utsccourse = utsc_course.find({"code":utsc_code})
    #     utmcourse = utm_course.find({"code":utm_code})
    #     info.append(utsgcourse)
    #     info.append(utsccourse)
    #     info.append(utmcourse)
    #     if not utsgcourse:
    #         utsg_code = data+"Y1"
    #         utsgcourse = utsg_course.find({"code":utsg_code})
    #         info.append(utsgcourse)
    #     if not utsccourse:
    #         utsc_code = data+"Y3"
    #         utsccourse = utsc_course.find({"code":utsc_code})
    #         info.append(utsccourse)
    #     if not utmcourse:
    #         utm_code = data+"Y5"
    #         utmcourse = utm_course.find({"code":utm_code})
    #         info.append(utmcourse)
    for i in utsgData:
        if i.get('code')==data:
            info.append(i)
            break;
        if i.get('code')==data+"H1":
            info.append(i)
            # data = data+"H1"
            break;
        if i.get('code')==data+"H1":
            info.append(i)
            # data = data+"H1"
            break;

    for j in utscData:
        if j.get('code')==data:
            info.append(j)
            break;
        if j.get('code')==data+"H3":
            info.append(j)
            # data = data+"H3"
            break;
        if j.get('code')==data+"Y3":
            info.append(j)
            # data = data+"Y3"
            break;

    for k in utmData:
        if k.get('code')==data:
            info.append(k)
            break;
        if k.get('code')==data+"H5":
            info.append(k)
            # data = data+"H5"
            break;
        if k.get('code')==data+"Y5":
            info.append(k)
            # data = data+"Y5"
            break;

    # Data = prereq.find_one({data: {'$exists' : True}})
    if info:
        if len(info)>1:
            return render_template("search_result.html", Data=info)
        else:
            url = url_for_campus(info[0]['campus'],info[0]['division'],info[0]['code'])
            return render_template("search_new.html", Data=info[0], url=url)
        # if Prereq:
        #     return render_template("search_results.html",Data = info,prereqs = Prereq[data])
        # else:
        #     return render_template("search_results.html",Data = info)
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
    app.run(host='0.0.0.0', port=5000, debug=True)
