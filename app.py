from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
client = MongoClient('mongodb://localhost', 27017)
db = client.test
test_db        = client.cobalt
utm_course     = test_db.utm_courses
utsc_course    = test_db.utsc_courses
utsg_course    = test_db.utsg_courses

@app.route('/')
def INDEX():
    return render_template("index.html")

@app.route('/search_queries')
def search_queries():

    data = request.args.get('query').upper()
    info=[]
    utm=utm_course.find({'code':{'$regex':'^'+data}}).batch_size(500)
    utsg=utsg_course.find({'code':{'$regex':'^'+data}}).batch_size(500)
    utsc=utsc_course.find({'code':{'$regex':'^'+data}}).batch_size(500)
    for i in utm:
        info.append({i["code"]:[i["name"],i["campus"]]})
    for i in utsg:
        info.append({i["code"]:[i["name"],i["campus"]]})
    for i in utsc:
        info.append({i["code"]:[i["name"],i["campus"]]})

    return jsonify(result=info)

@app.route('/api/search_queries')
def search_queries_api():

    data = request.args.get('query').upper()
    info=[]
    utm=utm_course.find({'code':{'$regex':'^'+data}}).batch_size(500)
    utsg=utsg_course.find({'code':{'$regex':'^'+data}}).batch_size(500)
    utsc=utsc_course.find({'code':{'$regex':'^'+data}}).batch_size(500)
    for i in utm:
        info.append({"code": i["code"], "name": i["name"]})
    for i in utsg:
        info.append({"code": i["code"], "name": i["name"]})
    for i in utsc:
        info.append({"code": i["code"], "name": i["name"]})
    return_data = {"result" :info}
    return jsonify(return_data)

@app.route('/search', methods=["POST", "GET"])
def search_post():
    data = request.args.get('course').upper()
    if len(data)<4:
        return render_template("/index.html")
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


@app.route('/api/search', methods=["POST", "GET"])
def searchdata():
    data = request.args.get('course').upper()
    if len(data)<4:
        return render_template("/index.html")
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
            return_data ={"code": info[0]['code'], "campus": info[0]['campus'], "description": info[0]["description"], "prerequisites": info[0]['prerequisites'], "name": info[0]['name'], "exclusions": info[0]["exclusions"], "prerequisites_array": info[0]["prerequisites_array"]}
            if "required_for" in info[0]:
                return_data["required_for"] = info[0]["required_for"]
            return jsonify(return_data)
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

def find_req_for(course):
    data = course.upper()
    utscData = utsc_course.find().batch_size(500)
    utmData = utm_course.find().batch_size(500)
    utsgData = utsg_course.find().batch_size(500)
    info =[]
    if data[3].isalpha():
        data = data[:3] + chr(ord(data[3])-16) + data[4:]
    
    if data[-1]=="1":
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
    elif data[-1]=="5":
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
    elif data[-1]=="3":
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
    try:
        return info[0]['required_for']
    except KeyError:
        return []

def build_tree_list(course, req_for):
    datadict = {}
    if len(req_for)==0:
        datadict["name"] = course
    else:
        datadict["name"] = course
        datadict["children"] = []
        for i in req_for:
            datadict["children"].append(build_tree_list(i, find_req_for(i)))
    return datadict
 
@app.route('/api/tree', methods=["POST", "GET"])
def tree_post1():
    data = request.args.get('course').upper()
    if len(data)<4:
        return render_template("/index.html")
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
            tree = build_tree_list(info[0]['code'], find_req_for(info[0]['code']))
            return jsonify(tree)
    else:
        return render_template("/index.html")


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
