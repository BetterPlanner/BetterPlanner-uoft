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
    Monday=[[],[]]
    Tuesday=[[],[]]
    Wednesday=[[],[]]
    Thursday=[[],[]]
    Friday=[[],[]]
    index=0
    for i in courses:
        if i['session']=="S":
            index=1
        elif i['session']=="Y":
            index=2

        #for j in courses:
        #get pracs #get tuts
        lectures =i['Sections']['lectures']
        for lecture in lectures:
            days = lecture['lect_day_time']
            for day in days:
                if day['day']=="Monday":
                    if index<1:
                        Monday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    elif index>1:
                        Monday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                        Monday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    else:
                        Monday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                elif day['day']=="Tuesday":
                    if index<1:
                        Tuesday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    elif index>1:
                        Tuesday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                        Tuesday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    else:
                        Tuesday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                elif day['day']=="Wednesday":
                    if index<1:
                        Wednesday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    elif index>1:
                        Wednesday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                        Wednesday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    else:
                        Wednesday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                elif day['day']=="Thursday":
                    if index<1:
                        Thursday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    elif index>1:
                        Thursday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                        Thursday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    else:
                        Thursday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                elif day['day']=="Friday":
                    if index<1:
                        Friday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    elif index==2:
                        Friday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                        Friday[0].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })
                    else:
                        Friday[1].append({
                            'course_name':i['course_name'],
                            'course_code':i['course_code'],
                            'lecture':lecture
                        })

    return 0

if __name__ == '__main__':
    CreateSchedule(["ANT102H5F","ANT101H5S"])
