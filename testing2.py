import requests
import json
import time
import pprint
from pymongo import MongoClient
rec_prereq = __import__('prerequisite')
client = MongoClient('localhost', 27017)

cobalt_db      = client.cobalt
cobalt_courses = cobalt_db.courses

test_db        = client.test

utm_courses    = test_db.utm_courses
utsg_courses   = test_db.utsg_courses
utsc_courses   = test_db.utsc_courses

prereq         = test_db.prereq

class main():
    def __init__(self):
        self.course_unique_utm = {}
        self.courses_unique_utsg = {}
        self.courses_unique_utsc = {}

        self.utm_courses()
        self.utsc_courses()
        self.utsg_courses()

    def utm_courses(self):
        utm_courses.drop()
        courses=[]
        for i in cobalt_courses.find({"campus": "UTM"}).distinct("name"):
            courses.append(i)
        for i in courses:
            a = False
            dic = cobalt_courses.find({"campus": "UTM", "name":i})
            # utm_courses.insert(dic[0])
            for j in dic:
                if len(j["code"])==9:
                    a = True
                    utm_courses.insert(j)
                    break

            if a==False:
                b=cobalt_courses.find({"campus": "UTM", "name":i})
                utm_courses.insert(b[0])

        print("utm done")
        # j = cobalt_courses.find({"code":courses[0], "campus": "UTM","term":'2019 Winter'})
        # pprint.pprint(j[0])


        # for i in courses:
        #     cobalt_courses.find({"campus": "UTM", "name")

    def utsg_courses(self):
        utsg_courses.drop()
        courses=[]
        for i in cobalt_courses.find({"campus": "UTSG"}).distinct("name"):
            courses.append(i)
        for i in courses:
            a=False
            dic = cobalt_courses.find({"campus": "UTSG", "name":i})
            for j in dic:
                if len(j["code"])==9:
                    utsg_courses.insert(j)
                    a = True
                    break
            if not a:
                b=cobalt_courses.find({"campus": "UTSG", "name":i})
                utsg_courses.insert(b[0])
        print("utsg done")
    def utsc_courses(self):
        utsc_courses.drop()
        courses=[]
        for i in cobalt_courses.find({"campus": "UTSC"}).distinct("name"):
            courses.append(i)
        for i in courses:
            a=False
            dic = cobalt_courses.find({"campus": "UTSC", "name":i})
            for j in dic:
                if len(j["code"])==9:
                    utsc_courses.insert(j)
                    a = True
                    break
            if not a:
                b=cobalt_courses.find({"campus": "UTSC", "name":i})
                utsc_courses.insert(b[0])
        print("utsc done")


if __name__ == '__main__':
    main()
