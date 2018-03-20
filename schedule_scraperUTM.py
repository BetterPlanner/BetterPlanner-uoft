import requests
import json
from pymongo import MongoClient
import pprint
# from bs4 import BeautifulSoup
rec_prereq = __import__('prerequisite')
client = MongoClient('localhost', 27017)
db = client.test
collection = db.schedules
coursesindb= db.courses


class Schedules_Parser():
    def __init__(self,course):
        self.course = course
        collection.drop()
        self.course_code_fix(course)

    def course_code_fix(self, course):
        lst = [] # each course can be offered in multiple seasons
        lst_text = []
        lst_summer = []
        session1 = "20179"
        session2 = "20185"
        session3 = "20189"
        rawstring  = "https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=" + session1 + "&courseCode=" + course.upper() + "&sname=&delivery=&courseTitle="
        # print(rawstring)
        raw_text = requests.get(rawstring)
        text = raw_text.content.decode("utf-8")
        if text.find("No matching courses")==-1:
            print("Reached")
            if text.find(course+"F")!=-1:
                lst.append(course+"F")
                current = text[text.find(course+"F"):]
                lst_text.append(current)
            if text.find(course+"S")!=-1:
                lst.append(course+"S")
                current = text[text.find(course+"S"):]
                lst_text.append(current)
            if text.find(course+"Y5Y")!=-1:
                lst.append(course+"Y5Y")
                current = text[text.find(course+"Y5Y"):]
                lst_text.append(current)
        else:
            rawstring="https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=" + session2 + "&courseCode=" + course.upper() + "&sname=&delivery=&courseTitle="
            raw_text = requests.get(rawstring)
            text = raw_text.content.decode("utf-8")
            if text.find("No matching courses")!=-1:
                if text.find(course+"F")!=-1:
                    lst_summer.append(course+"F")
                if text.find(course+"S")!=-1:
                    lst_summer.append(course+"S")
        count=0
        for i in lst:
            # print("foor loop")
            parser = startParser(i,lst_text[count])
            count+=1
            if parser!=0:
                return -1
        return 1

def startParser(course, text):
    current_course_dict={}
    lectures={}
    current_lecture={}
    tableDayList = []
    roomList = []
    lect_day_time={}
    sections={}
    # insert course name
    text = text[text.find("h4")+3:]
    coursename= text[:text.find("<b>")]
    current_course_dict["course name"]= coursename
    # insert session
    current_course_dict["session"]=  coursename[8]
    print("course name " +coursename + "\n")
    table = text[text.find("tbl_"+course+"LEC")+12:text.find("</table>")]
    while(table.find("id='"+"tr_"+course+"LEC") != -1):
        table = table[table.find("tr_")+12:] #start table parsing
        tableLecture = table[:table.find("class")-2] #grab lecture number
        # print("Lecture " +tableLecture)

        tableinst = table[table.find("instrTD")+10:]
        tableinst = tableinst[:tableinst.find("/td")] #getting instructor name
        #print("table instructor "+tableinst)
        while(tableinst.find("<br>") != -1):
            instructor = tableinst[:tableinst.find("<br>")].replace(" ","")
            tableinst=tableinst[tableinst.find("<br>")+4:]
            # print("instructor1: " +instructor.strip())
            current_lecture["instructors"]=instructor.strip()
            # instructorList.append(instructor.strip())
            table=table[table.find("<br>")+4:]
        table = table[table.find("enrolTD")+10:]
        tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
        # print(tableEnr.strip())
        tableEnr =tableEnr.strip()
        tableEnr = tableEnr.split(",")
        tableEnr[0]=tableEnr[0].split("/")
        tableEnr[1]=tableEnr[1].split(":")
        # e.g [['39', '150'], ['wait', '0']]
        current_lecture["enrollement"]={"enrolled":tableEnr[0][0], "capacity":tableEnr[0][1], tableEnr[1][0]:tableEnr[1][1]}

        table = table[table.find("<abbr title")+13:] #what day the lecture happens
        tableday = table[:table.find("</td")]
        firstday = tableday[:tableday.find("</abbr") - 4]
        firstday.replace("\r"," ").replace("\n"," ").replace("\t"," ")
        tableDayList.append(firstday)
        print(firstday)
        while(tableday.find("<abbr")!=-1):

            tableday = tableday[tableday.find("<abbr")+13:]
            courseday = tableday[:tableday.find("</abbr")-4]
            print(courseday)
            tableDayList.append(tableday[:tableday.find("</abbr")-4])
            tableday = tableday[tableday.find("</abbr")+7:]
        #days list for current lecture
        # current_lecture["lecture_days"]=tableDayList

        table = table[table.find("start_time")+12:]
        tableStart = table[:table.find("</td>")]
        # print("day:")
        # print(len(tableDayList))

        lstOfTime = []
        startTimeList = []
        endTimeList = []
        while (tableStart.find("<br>")!= -1): #Start time
            # print(tableStart[:tableStart.find("<br>")].strip())
            startTimeList.append(tableStart[:tableStart.find("<br>")].strip())
            tableStart = tableStart[tableStart.find("<br>")+4:]
        #print("Start time"+startTimeList[0])
        table = table[table.find("</td>")+4:]
        tableEnd = table[:table.find("</td>")]
        firstEnd = tableEnd[20:tableEnd.find("<br>")].strip()
        endTimeList.append(firstEnd)
        tableEnd = tableEnd[tableEnd.find("<br>")+4:]
        while (tableEnd.find("<br>")!= -1): #End time
            endTimeList.append(tableEnd[:tableEnd.find("<br>")].strip())
            tableEnd = tableEnd[tableEnd.find("<br>")+4:]
        for z in range (0,len(tableDayList)):
            lstOfTime.append((startTimeList[z],endTimeList[z]))
        # lectures array e.g [('10:00', '11:00'), ('09:00', '11:00')]
        # current_lecture["lecture_times"]=lstOfTime

        table = table[table.find("<td>")+13:]
        table = table[table.find("<td>")+4:]
        tableRoom = table[:table.find("/td")]
        while (tableRoom.find("<br>") != -1):  # Start time
            roomNum = tableRoom[:tableRoom.find("<br>")].strip()
            if roomNum.find("</a>")>0:
                roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
            else:
                roomList.append(roomNum)
            tableRoom = tableRoom[tableRoom.find("<br>")+4:]
        current_lecture["rooms"]=roomList
        for i in range(0,len(tableDayList)):
            time={"start":lstOfTime[i][0], "end":lstOfTime[i][1]}
            lect_day_time[tableDayList[i]]=time
        current_lecture["lect_day_time"]=lect_day_time
        lectures[tableLecture]=current_lecture
        current_lecture={}
        lect_day_time={}
        startTimeList = []
        endTimeList = []
        roomList = []
        tableDayList =[]
    sections["lectures"]=lectures
    if (table.find("tr_" + course + "TUT") != -1):
        tutTable = table[table.find("tr_" + course + "TUT"):]
        lstOfTutorials = tut_scraper(course, tutTable)
        sections["Tutorials"]=lstOfTutorials

    if (table.find("tr_" + course +"PRA") != -1):
        PRATable = table[table.find("tr_" + course + "PRA"):]
        lstOfPRA = pra_scraper(course, PRATable)
        sections["Practicals"]=lstOfPRA
    current_course_dict["Sections"]=sections
    collection.insert(current_course_dict)
    return 0

def pra_scraper(course ,table): #course is a list
    lstofDic = []
    practicals={}
    current_practical={}
    tableDayList = []
    roomList = []
    prac_day_time={}
    #Capitalize the course code

    i=course
    instructorList = []
    roomList = []
    tableDayList = []
    lectureDic = {}
    #print(table)
    while(table.find("<label for='"+course+"PRA") != -1):
        table = table[table.find("tr_")+12:] #start table parsing
        tableLecture = table[:table.find("class")-2] #grab lecture number
        # print("Lecture" +tableLecture)

        table = table[table.find("enrolTD")+10:]
        tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
        # print(tableEnr.strip())
        tableEnr =tableEnr.strip()
        tableEnr = tableEnr.split(",")
        tableEnr[0]=tableEnr[0].split("/")
        tableEnr[1]=tableEnr[1].split(":")
        # e.g [['39', '150'], ['wait', '0']]
        current_practical["enrollement"]={"enrolled":tableEnr[0][0], "capacity":tableEnr[0][1], tableEnr[1][0]:tableEnr[1][1]}


        table = table[table.find("<abbr title")+13:] #what day the lecture happens
        tableday = table[:table.find("</td")]
        firstday = tableday[:tableday.find("</abbr") - 4]
        firstday.replace("\r"," ").replace("\n"," ").replace("\t"," ")
        tableDayList.append(firstday)
        tableday = tableday[tableday.find("</abbr")+4:]
        # print(tableday)
        while(tableday.find("<abbr")!=-1):
            tableday = tableday[tableday.find("<abbr")+13:]
            courseday = tableday[:tableday.find("</abbr")-4]
            # print(courseday)
            tableDayList.append(tableday[:tableday.find("</abbr")-4])
            tableday = tableday[tableday.find("</abbr")+7:]
        #print(tableDayList)
        table = table[table.find("start_time")+12:]
        tableStart = table[:table.find("</td>")]
        # print("day:")
        # print(tableDayList)
        lstOfTime = []
        startTimeList = []
        endTimeList = []
        while (tableStart.find("<br>")!= -1): #Start time
            # print(tableStart[:tableStart.find("<br>")].strip())
            startTimeList.append(tableStart[:tableStart.find("<br>")].strip())
            tableStart = tableStart[tableStart.find("<br>")+4:]
        #print("Start time"+startTimeList[0])
        table = table[table.find("</td>")+4:]
        tableEnd = table[:table.find("</td>")]
        firstEnd = tableEnd[20:tableEnd.find("<br>")].strip()
        endTimeList.append(firstEnd)
        tableEnd = tableEnd[tableEnd.find("<br>")+4:]
        while (tableEnd.find("<br>")!= -1): #End time
            endTimeList.append(tableEnd[:tableEnd.find("<br>")].strip())
            tableEnd = tableEnd[tableEnd.find("<br>")+4:]
        for z in range (0,len(tableDayList)):
            lstOfTime.append((startTimeList[z],endTimeList[z]))
        # print(lstOfTime)
        table = table[table.find("<td>")+13:]
        table = table[table.find("<td>")+4:]
        tableRoom = table[:table.find("/td")]
        while (tableRoom.find("<br>") != -1):  # Start time
            roomNum = tableRoom[:tableRoom.find("<br>")].strip()
            # print(roomNum)
            if roomNum.find("</a>")>0:
                roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
            else:
                roomList.append(roomNum)
            tableRoom = tableRoom[tableRoom.find("<br>")+4:]
        current_practical["room"]=roomList
        for i in range(0,len(tableDayList)):
            time={"start":lstOfTime[i][0], "end":lstOfTime[i][1]}
            prac_day_time[tableDayList[i]]=time
        current_practical["prac_day_time"]=prac_day_time
        practicals[tableLecture]=current_practical
        current_practical={}
        prac_day_time={}
        startTimeList = []
        endTimeList = []
        roomList = []
        tableDayList =[]
    return practicals

def tut_scraper(course ,table): #course is a list
    lstofDic = []
    tuts={}
    current_tut={}
    tableDayList = []
    roomList = []
    tut_day_time={}
    #Capitalize the course code

    i=course
    instructorList = []
    roomList = []
    tableDayList = []
    lectureDic = {}

    while(table.find("<label for='"+course+"TUT") != -1):
        table = table[table.find("tr_")+12:] #start table parsing
        tableLecture = table[:table.find("class")-2] #grab lecture number
        # print("Lecture" +tableLecture)

        table = table[table.find("enrolTD")+10:]
        tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
        # print(tableEnr.strip())
        tableEnr =tableEnr.strip()
        tableEnr = tableEnr.split(",")
        tableEnr[0]=tableEnr[0].split("/")
        tableEnr[1]=tableEnr[1].split(":")
        # e.g [['39', '150'], ['wait', '0']]
        current_tut["enrollement"]={"enrolled":tableEnr[0][0], "capacity":tableEnr[0][1], tableEnr[1][0]:tableEnr[1][1]}

        table = table[table.find("<abbr title")+13:] #what day the lecture happens
        tableday = table[:table.find("</td")]
        firstday = tableday[:tableday.find("</abbr") - 4]
        firstday.replace("\r"," ").replace("\n"," ").replace("\t"," ")
        tableDayList.append(firstday)
        tableday = tableday[tableday.find("</abbr")+4:]
        # print(tableday)
        while(tableday.find("<abbr")!=-1):
            tableday = tableday[tableday.find("<abbr")+13:]
            courseday = tableday[:tableday.find("</abbr")-4]
            # print(courseday)
            tableDayList.append(tableday[:tableday.find("</abbr")-4])
            tableday = tableday[tableday.find("</abbr")+7:]
        #print(tableDayList)
        table = table[table.find("start_time")+12:]
        tableStart = table[:table.find("</td>")]
        # print("day:")
        # print(tableDayList)
        lstOfTime = []
        startTimeList = []
        endTimeList = []
        while (tableStart.find("<br>")!= -1): #Start time
            # print(tableStart[:tableStart.find("<br>")].strip())
            startTimeList.append(tableStart[:tableStart.find("<br>")].strip())
            tableStart = tableStart[tableStart.find("<br>")+4:]
        #print("Start time"+startTimeList[0])
        table = table[table.find("</td>")+4:]
        tableEnd = table[:table.find("</td>")]
        firstEnd = tableEnd[20:tableEnd.find("<br>")].strip()
        endTimeList.append(firstEnd)
        tableEnd = tableEnd[tableEnd.find("<br>")+4:]
        while (tableEnd.find("<br>")!= -1): #End time
            endTimeList.append(tableEnd[:tableEnd.find("<br>")].strip())
            tableEnd = tableEnd[tableEnd.find("<br>")+4:]
        for z in range (0,len(tableDayList)):
            lstOfTime.append((startTimeList[z],endTimeList[z]))
        # print(lstOfTime)
        table = table[table.find("<td>")+13:]
        table = table[table.find("<td>")+4:]
        tableRoom = table[:table.find("/td")]
        while (tableRoom.find("<br>") != -1):  # Start time
            roomNum = tableRoom[:tableRoom.find("<br>")].strip()
            # print(roomNum)
            if roomNum.find("</a>")>0:
                roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
            else:

                roomList.append(roomNum)
            tableRoom = tableRoom[tableRoom.find("<br>")+4:]
        current_tut["room"]=roomList
        for i in range(0,len(tableDayList)):
            time={"start":lstOfTime[i][0], "end":lstOfTime[i][1]}
            tut_day_time[tableDayList[i]]=time
        current_tut["tut_day_time"]=tut_day_time
        tuts[tableLecture]=current_tut
        current_tut={}
        tut_day_time={}
        startTimeList = []
        endTimeList = []
        roomList = []
        tableDayList = []
    return tuts




if __name__ == '__main__':
    # for i in coursesindb.find():
    #     Schedules_Parser(i["course code"])
    #     pprint.pprint(i["course code"])
    Schedules_Parser("CHM110H5")
    print("done")
