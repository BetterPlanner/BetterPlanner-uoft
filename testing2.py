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
        utm_courses.drop()
        self.utm_courses()

    def utm_courses(self):
        courses=[]
        for i in cobalt_courses.find({"campus": "UTM"}).distinct("code"):
            if(len(i)==9):
                courses.append(i)
        for i in courses:
            dic = cobalt_courses.find({"campus": "UTM", "code":i})

            utm_courses.insert(dic[0])

        # j = cobalt_courses.find({"code":courses[0], "campus": "UTM","term":'2019 Winter'})
        # pprint.pprint(j[0])


        # for i in courses:
        #     cobalt_courses.find({"campus": "UTM", "name")





if __name__ == '__main__':
    main()
