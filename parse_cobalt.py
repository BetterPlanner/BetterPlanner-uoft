import requests
import json
import time
import pprint
from pymongo import MongoClient
rec_prereq = __import__('necessary_for')
client = MongoClient('localhost', 27017)

cobalt_db      = client.cobalt
cobalt_courses = cobalt_db.courses

test_db        = client.test

utm_extra    = test_db.utm_extra
utsg_extra   = test_db.utsg_extra
utsc_extra   = test_db.utsc_extra

utm_courses     = test_db.utm_course

utm_courses     = test_db.utm_courses
utsc_courses    = test_db.utsc_courses
utsg_courses    = test_db.utsg_courses
prereq         = test_db.prereq

class main():
    def __init__(self):
        self.course_unique_utm = {}
        self.courses_unique_utsg = {}
        self.courses_unique_utsc = {}

        self.recognized_dict={}

        self.utm_course_list = []
        self.utsc_course_list = []
        self.utsg_course_list = []

        self.utm_courses()
        self.utsc_courses()
        self.utsg_courses()
        # self.utm()

    def utm(self):
        utm_extra.drop()
        course = []
        courses=[]
        for i in cobalt_courses.find({"campus": "UTM"}).distinct("code"):
            if i[:8] not in course:
                courses.append(i)
                course.append(i[:8])


        for i in courses:
            a = False
            dic = cobalt_courses.find({"campus": "UTM", "code":i})
            # utm_courses.insert(dic[0])
            for j in dic:
                if len(j["code"])==9:
                    a = True
                    utm_extra.insert(j)
                    break

            if a==False:
                b=cobalt_courses.find({"campus": "UTM", "code":i})
                utm_extra.insert(b[0])
        utm_courses.drop()

        for i in utm_extra.find():
            j = i
            j["code"]=i["code"][:8]
            utm_courses.insert(j)
            self.utm_course_list.append(j)
        utm_extra.drop()
        self.run_prereq_utm()
        print("utm done")

    def utm_courses(self):
        utm_extra.drop()
        courses=[]
        course = []
        for i in cobalt_courses.find({"campus": "UTM"}).distinct("code"):
            if i[:8] not in course:
                courses.append(i)
                course.append(i[:8])
        for i in courses:
            a = False
            dic = cobalt_courses.find({"campus": "UTM", "code":i})
            # utm_courses.insert(dic[0])
            for j in dic:
                if len(j["code"])==9:
                    a = True
                    utm_extra.insert(j)
                    break

            if a==False:
                b=cobalt_courses.find({"campus": "UTM", "code":i})
                utm_extra.insert(b[0])
        utm_courses.drop()

        for i in utm_extra.find():
            j = i
            j["code"]=i["code"][:8]
            utm_courses.insert(j)
            self.utm_course_list.append(j)
        utm_extra.drop()
        self.run_prereq_utm()
        print("utm done")

    def utsg_courses(self):
        utsg_extra.drop()
        courses=[]
        course = []
        for i in cobalt_courses.find({"campus": "UTSG"}).distinct("code"):
            if i[:8] not in course:
                courses.append(i)
                course.append(i[:8])
        for i in courses:
            a=False
            dic = cobalt_courses.find({"campus": "UTSG", "code":i})
            for j in dic:
                if len(j["code"])==9:
                    utsg_extra.insert(j)
                    a = True
                    break
            if not a:
                b=cobalt_courses.find({"campus": "UTSG", "code":i})
                utsg_extra.insert(b[0])
        utsg_courses.drop()
        for i in utsg_extra.find():
            j = i
            j["code"]=i["code"][:8]
            utsg_courses.insert(j)
            self.utsg_course_list.append(j)
        utsg_extra.drop()
        self.run_prereq_utsg()
        print("utsg done")

    def utsc_courses(self):
        utsc_extra.drop()
        courses=[]
        course = []
        for i in cobalt_courses.find({"campus": "UTSC"}).distinct("code"):
            if i[:8] not in course:
                courses.append(i)
                course.append(i[:8])
        for i in courses:
            a=False
            dic = cobalt_courses.find({"campus": "UTSC", "code":i})
            for j in dic:
                if len(j["code"])==9:
                    utsc_extra.insert(j)
                    a = True
                    break
            if not a:
                b=cobalt_courses.find({"campus": "UTSC", "code":i})
                utsc_extra.insert(b[0])
        utsc_courses.drop()
        for i in utsc_extra.find():
            j = i
            j["code"]=i["code"][:8]
            utsc_courses.insert(j)
            self.utsc_course_list.append(j)
        utsc_extra.drop()
        self.run_prereq_utsc()
        print("utsc done")

    def run_prereq_utm(self):
        self.recognized_dict = rec_prereq.recognized_prereq_utm(self.utm_course_list,self.recognized_dict)
        self.add_required_for(utm_courses)
        self.recognized_dict = {}

    def run_prereq_utsc(self):
        self.recognized_dict = rec_prereq.recognized_prereq_utsc(self.utsc_course_list,self.recognized_dict)
        self.add_required_for(utsc_courses)
        self.recognized_dict = {}

    def run_prereq_utsg(self):
        self.recognized_dict = rec_prereq.recognized_prereq_utsg(self.utsg_course_list,self.recognized_dict)
        self.add_required_for(utsg_courses)
        self.recognized_dict = {}

    def add_required_for(self,campus):
        for i in self.recognized_dict:
            campus.update_one({"code":i}, {'$set': {"required_for":self.recognized_dict[i]}})


if __name__ == '__main__':
    main()
