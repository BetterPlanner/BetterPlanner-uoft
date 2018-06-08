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

    def utm_courses(self):
        courses=[]
        for i in cobalt_courses.find('name', {"campus": "UTM"}):
            pprint.pprint(i)
        # for i in courses:
        #     cobalt_courses.find({"campus": "UTM", "name")





if __name__ == '__main__':
    main()
