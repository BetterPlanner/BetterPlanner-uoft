import requests
import json
from pymongo import MongoClient
# from bs4 import BeautifulSoup
#rec_prereq = __import__('prerequisite')
client = MongoClient('localhost', 27017) #connect to our mongoclient
db = client.test
scheduleCollection = db.schedules # we call from a database called schedule
courseCollection = db.courses


def CreateSchedule(courses): #list of courses used to create a schedule returns a list of combinations
    course_objects =[]
    for i in courses:
        courseData = scheduleCollection.find_one({'course_code': i})
        if courseData:
            course_objects.append(courseData)

    TimeTable(course_objects)
    # courseData = scheduleCollection.find_one({'course_code': courses}) # .find_one({'course code':data})
    # print(courseData)
    return 0



def TimeTable(courses):
    schedule =[];
    practical =0;
    tutorial =0;
    Monday=[]
    Tuesday=[]
    Wednesday=[]
    Thursday=[]
    Friday=[]
    for i in courses:
        #for j in courses:
        #get pracs #get tuts
        lectures =i['Sections']['lectures']
        for lecture in lectures:
            days = lecture['lect_day_time']
            for day in days:
                if day['day']=="Monday":
                    Monday.append({
                        'course_name':i['course_name'],
                        'course_code':i['course_code'],
                        'lecture':lecture
                    })
                elif day['day']=="Tuesday":
                    Tuesday.append({
                        'course_name':i['course_name'],
                        'course_code':i['course_code'],
                        'lecture':lecture
                    })
                elif day['day']=="Wednesday":
                    Wednesday.append({
                        'course_name':i['course_name'],
                        'course_code':i['course_code'],
                        'lecture':lecture
                    })
                elif day['day']=="Thursday":
                    Thursday.append({
                        'course_name':i['course_name'],
                        'course_code':i['course_code'],
                        'lecture':lecture
                    })
                elif day['day']=="Friday":
                    Friday.append({
                        'course_name':i['course_name'],
                        'course_code':i['course_code'],
                        'lecture':lecture
                    })
    return 0

if __name__ == '__main__':
    CreateSchedule(["ANT102H5F","ANT101H5S"])
