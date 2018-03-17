import requests
def HTMLParser(course): #creates a list of dicitonaries for a course
    lstofDic = []
    course = ["CSC258H5S"]
    #Capitalize the course code
    #https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20185&courseCode=CSC148H5%2CCHM485H5%2CANT101H5&sname=&delivery=&courseTitle= #3 courses
    #https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20185&courseCode=CSC148H5%2CCHM485H5&sname=&delivery=&courseTitle= #2 courses
    #raw_text = requests.get("https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20179&courseCode=CSC108H5&sname=&delivery=&courseTitle=")
    #raw_text = requests.get("https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20179&courseCode=LIN203H5&sname=&delivery=&courseTitle=")
    raw_text = requests.get("https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20179&courseCode=CSC258H5&sname=&delivery=&courseTitle=")
    text = raw_text.content.decode("utf-8")

    #print(text)
    for i in course:
        instructorList = []
        roomList = []
        tableDayList = []
        lectureDic = {}
        text = text[text.find(i):]  # we cut text to make the file shorter
        text = text[text.find("h4")+3:]
        coursename= text[:text.find("<b>")]
        print("course name" +coursename + "\n")
        table = text[text.find("tbl_"+i+"LEC")+12:text.find("</table>")]

        #print(table)
        #print("id='"+"tr_"+i+"H5FLEC")
        #print(table.find("id='tr_CSC108H5FLEC"))
        while(table.find("id='"+"tr_"+i+"LEC") != -1):
            #tr = 'tr_'+i
            #print(tr)
            table = table[table.find("tr_")+12:] #start table parsing
            tableLecture = table[:table.find("class")-2] #grab lecture number
            print("Lecture" +tableLecture)
            tableinst = table[table.find("instrTD")+10:]
            tableinst = tableinst[:tableinst.find("/td")] #getting instructor name
            #print("table instructor "+tableinst)
            while(tableinst.find("<br>") != -1):
                instructor = tableinst[:tableinst.find("<br>")].replace(" ","")
                tableinst=tableinst[tableinst.find("<br>")+4:]
                print("instructor:" +instructor.strip())
                instructorList.append(instructor)
                table=table[table.find("<br>")+4:]
            table = table[table.find("enrolTD")+10:]
            tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
            print(tableEnr.strip())
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
            #print(tableDayList)
            table = table[table.find("start_time")+12:]
            tableStart = table[:table.find("</td>")]
            print("day:")
            print(len(tableDayList))
            lstOfTime = []
            startTimeList = []
            endTimeList = []
            while (tableStart.find("<br>")!= -1): #Start time
                print(tableStart[:tableStart.find("<br>")].strip())
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
            print(lstOfTime)
            table = table[table.find("<td>")+13:]
            table = table[table.find("<td>")+4:]
            tableRoom = table[:table.find("/td")]
            while (tableRoom.find("<br>") != -1):  # Start time
                roomNum = tableRoom[:tableRoom.find("<br>")].strip()
                print(roomNum)
                roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
                tableRoom = tableRoom[tableRoom.find("floor map for") + 13:]

            lectureDic["instructorlist"]=instructorList
            lectureDic["startTimeList"] = startTimeList
            lectureDic["endTimeList"] = endTimeList
            lectureDic["roomList"] = roomList
            lectureDic["tableDayList"] = tableDayList
            lstofDic.append(lectureDic)
            instructorList =[]
            startTimeList = []
            endTimeList = []
            roomList = []
            tableDayList =[]
    #print(table)
    if (table.find("tr_" + i + "TUT") != -1):
        tutTable = table[table.find("tr_" + i + "TUT"):]
        lstOfTutorials = tut_scraper(i, tutTable)
    if (table.find("tr_" + i +"PRA") != -1):
        PRATable = table[table.find("tr_" + i + "PRA"):]
        lstOfPRA = pra_scraper(i, PRATable)

def pra_scraper(course ,table): #course is a list
    lstofDic = []
    #Capitalize the course code
    print("practical")
    i=course
    instructorList = []
    roomList = []
    tableDayList = []
    lectureDic = {}
    #print(table)
    while(table.find("<label for='"+course+"PRA") != -1):
        #table = table[table.find("<label for='"+course+"H5F"+"PRA")+30:]
        #praLec = table[:table.find("</label")]
        #print(praLec)
        #print(tr)
        table = table[table.find("tr_")+12:] #start table parsing
        tableLecture = table[:table.find("class")-2] #grab lecture number
        print("Lecture" +tableLecture)
        #tableinst = table[table.find("instrTD")+10:]
        #tableinst = tableinst[:tableinst.find("/td")] #getting instructor name
        #print("table instructor "+tableinst)
        #while(tableinst.find("<br>") != -1):
        #    instructor = tableinst[:tableinst.find("<br>")].replace(" ","")
        #    tableinst=tableinst[tableinst.find("<br>")+4:]
        #    print("instructor:" +instructor.strip())
        #    instructorList.append(instructor)
        #    table=table[table.find("<br>")+4:]
        table = table[table.find("enrolTD")+10:]
        tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
        print(tableEnr.strip())
        table = table[table.find("<abbr title")+13:] #what day the lecture happens
        tableday = table[:table.find("</td")]
        firstday = tableday[:tableday.find("</abbr") - 4]
        firstday.replace("\r"," ").replace("\n"," ").replace("\t"," ")
        tableDayList.append(firstday)
        tableday = tableday[tableday.find("</abbr")+4:]
        print(tableday)
        while(tableday.find("<abbr")!=-1):
            tableday = tableday[tableday.find("<abbr")+13:]
            courseday = tableday[:tableday.find("</abbr")-4]
            print(courseday)
            tableDayList.append(tableday[:tableday.find("</abbr")-4])
            tableday = tableday[tableday.find("</abbr")+7:]
        #print(tableDayList)
        table = table[table.find("start_time")+12:]
        tableStart = table[:table.find("</td>")]
        print("day:")
        print(tableDayList)
        lstOfTime = []
        startTimeList = []
        endTimeList = []
        while (tableStart.find("<br>")!= -1): #Start time
            print(tableStart[:tableStart.find("<br>")].strip())
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
        print(lstOfTime)
        table = table[table.find("<td>")+13:]
        table = table[table.find("<td>")+4:]
        tableRoom = table[:table.find("/td")]
        while (tableRoom.find("<br>") != -1):  # Start time
            roomNum = tableRoom[:tableRoom.find("<br>")].strip()
            print(roomNum)
            roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
            tableRoom = tableRoom[tableRoom.find("floor map for") + 13:]

        lectureDic["startTimeList"] = startTimeList
        lectureDic["endTimeList"] = endTimeList
        lectureDic["roomList"] = roomList
        lectureDic["tableDayList"] = tableDayList
        lstofDic.append(lectureDic)
        startTimeList = []
        endTimeList = []
        roomList = []
        tableDayList = []
def tut_scraper(course ,table): #course is a list
    lstofDic = []
    #Capitalize the course code
    print("tut")
    i=course
    instructorList = []
    roomList = []
    tableDayList = []
    lectureDic = {}
    #print(table)
    while(table.find("<label for='"+course+"TUT") != -1):
        #table = table[table.find("<label for='"+course+"H5F"+"PRA")+30:]
        #praLec = table[:table.find("</label")]
        #print(praLec)
        #print(tr)
        table = table[table.find("tr_")+12:] #start table parsing
        tableLecture = table[:table.find("class")-2] #grab lecture number
        print("Lecture" +tableLecture)
        #tableinst = table[table.find("instrTD")+10:]
        #tableinst = tableinst[:tableinst.find("/td")] #getting instructor name
        #print("table instructor "+tableinst)
        #while(tableinst.find("<br>") != -1):
        #    instructor = tableinst[:tableinst.find("<br>")].replace(" ","")
        #    tableinst=tableinst[tableinst.find("<br>")+4:]
        #    print("instructor:" +instructor.strip())
        #    instructorList.append(instructor)
        #    table=table[table.find("<br>")+4:]
        table = table[table.find("enrolTD")+10:]
        tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
        print(tableEnr.strip())
        table = table[table.find("<abbr title")+13:] #what day the lecture happens
        tableday = table[:table.find("</td")]
        firstday = tableday[:tableday.find("</abbr") - 4]
        firstday.replace("\r"," ").replace("\n"," ").replace("\t"," ")
        tableDayList.append(firstday)
        tableday = tableday[tableday.find("</abbr")+4:]
        print(tableday)
        while(tableday.find("<abbr")!=-1):
            tableday = tableday[tableday.find("<abbr")+13:]
            courseday = tableday[:tableday.find("</abbr")-4]
            print(courseday)
            tableDayList.append(tableday[:tableday.find("</abbr")-4])
            tableday = tableday[tableday.find("</abbr")+7:]
        #print(tableDayList)
        table = table[table.find("start_time")+12:]
        tableStart = table[:table.find("</td>")]
        print("day:")
        print(tableDayList)
        lstOfTime = []
        startTimeList = []
        endTimeList = []
        while (tableStart.find("<br>")!= -1): #Start time
            print(tableStart[:tableStart.find("<br>")].strip())
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
        print(lstOfTime)
        table = table[table.find("<td>")+13:]
        table = table[table.find("<td>")+4:]
        tableRoom = table[:table.find("/td")]
        while (tableRoom.find("<br>") != -1):  # Start time
            roomNum = tableRoom[:tableRoom.find("<br>")].strip()
            print(roomNum)
            roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
            tableRoom = tableRoom[tableRoom.find("floor map for") + 13:]

        lectureDic["startTimeList"] = startTimeList
        lectureDic["endTimeList"] = endTimeList
        lectureDic["roomList"] = roomList
        lectureDic["tableDayList"] = tableDayList
        lstofDic.append(lectureDic)
        startTimeList = []
        endTimeList = []
        roomList = []
        tableDayList = []
HTMLParser("asd")