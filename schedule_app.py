import requests
import json
from pymongo import MongoClient
# from bs4 import BeautifulSoup
#rec_prereq = __import__('prerequisite')
client = MongoClient('localhost', 27017) #connect to our mongoclient
db = client.test
scheduleCollection = db.schedules # we call from a database called schedule
courseCollection = db.courses
# we need to communicate the website and database
# first we will need to grab courses from the database
# second we must create combinations of schedules based on lecture times and days that do not conflict

#A section has a key lectures, lectures has a key 0101,0102...  lectures has an enrolement,instructors, lect_daytime: mon,tues as keys...,start and end in side the days
#rooms is a list
def CreateSchedule(courses): #list of courses used to create a schedule returns a list of combinations
    courseData = scheduleCollection.find().batch_size(1100)  # .find_one({'course code':data})
    scheduleList = [];
    for i in courses:
        for d in courseData:
            if i == d:
                scheduleList.append(d)
    TimeTable(scheduleList)
def TimeTable(courses):
    schedule =[];
    practical =0;
    tutorial =0;
    for i in courses:
        #for j in courses:
        #get pracs #get tuts
        Monday=[]
        Tuesday=[]
        Wednesday=[]
        Thursday=[]
        Friday=[]

        if i["lect_day_time"]["Monday"]:
            coursed={}
            coursed["course_name"]=i["course_name"]
            coursed["course_name"]["start"]=i["lect_day_time"]["start"]
            coursed["course_name"]["end"]=i["lect_day_time"]["end"]
            Monday.append(coursed)
        if i["lect_day_time"]["Tuesday"]:
            coursed = {}
            coursed["course_name"] = i["course_name"]
            coursed["course_name"]["start"] = i["lect_day_time"]["start"]
            coursed["course_name"]["end"] = i["lect_day_time"]["end"]
            Tuesday.append(coursed)
        if i["lect_day_time"]["Wednesday"]:
            coursed = {}
            coursed["course_name"] = i["course_name"]
            coursed["course_name"]["start"] = i["lect_day_time"]["start"]
            coursed["course_name"]["end"] = i["lect_day_time"]["end"]
            Wednesday.append(coursed)
        if i["lect_day_time"]["Thursday"]:
            coursed = {}
            coursed["course_name"] = i["course_name"]
            coursed["course_name"]["start"] = i["lect_day_time"]["start"]
            coursed["course_name"]["end"] = i["lect_day_time"]["end"]
            Thursday.append(coursed)
        if i["lect_day_time"]["Friday"]:
            coursed = {}
            coursed["course_name"] = i["course_name"]
            coursed["course_name"]["start"] = i["lect_day_time"]["start"]
            coursed["course_name"]["end"] = i["lect_day_time"]["end"]
            Friday.append(coursed)
        weekend = {}
        weekend["monday"]= Monday
        weekend["tuesday"]= Tuesday
        weekend["wednesday"] = Wednesday
        weekend["thursday"] = Thursday
        weekend["friday"] = Friday
        helper(weekend,courses)
def helper(week,courses): #takes in a dict called week
    schedule = []
    for i in courses:
        if i not in schedule:
            if week["monday"][i]:
                pass
            elif week["tuesday"][i]:
                pass
            elif week["wednesday"][i]:
                pass
            elif week["thursday"][i]:
                pass
            elif week["friday"][i]:
                pass
def checktimes(time,time2): #times are strings [00:00] format
    hour1 = time[0:1]


