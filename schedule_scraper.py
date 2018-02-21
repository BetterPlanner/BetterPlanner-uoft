import requests
def HTMLParser(course): #course is a list
    lstofDic = []
    course = ["CSC108"]

    raw_text = requests.get("https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20179&courseCode=CSC108H5&sname=&delivery=&courseTitle=")
    text = raw_text.content.decode("utf-8")

    #print(text)
    for i in course:
        instructorList = []
        startTimeList = []
        endTimeList = []
        roomList = []
        tableDayList = []
        
        lectureDic = {}
        text = text[text.find(i):]  # we cut text to make the file shorter
        text = text[text.find("h4")+3:]
        coursename= text[:text.find("h4")]

        table = text[text.find("tbl_"+i)+12:text.find("</table>")]
        while(table.find("tr id") != -1):
            table = table[table.find("tr id")+10:] #start table parsing
            tableLecture = table[:table.find("class")-2] #grab lecture number
            print(tableLecture)
            tableinst = table[table.find("instrTD")+10:]
            tableinst = tableinst[:tableinst.find("/td")] #getting instructor name
            print("table instructor "+tableinst)
            while(tableinst.find("<br>") != -1):
                instructor = tableinst[:tableinst.find("<br>")].replace(" ","")
                tableinst=tableinst[tableinst.find("<br>")+4:]
                print(instructor)
                instructorList.append(instructor)
                table=table[table.find("<br>")+4:]
            table = table[table.find("enrolTD")+10:]
            tableEnr = table[:table.find("</td>")].replace(" ","")#table enrol people who are enrolled and waitlisted
            print(tableEnr)
            table = table[table.find("<abbr title")+12:] #what day the lecture happens

            tableday = table[:table.find("</td")]

            while(tableday.find("<abbr")!=-1):
                tableday = tableday[tableday.find("<abbr")+13:]
                tableDayList.append(tableday[:tableday.find("</abbr")-4])
                tableday = tableday[tableday.find("</abbr")+7:]
            print(tableDayList)
            table = table[table.find("start_time")+12:]
            tableStart = table[:table.find("</td>")]

            while (tableStart.find("<br>")!= -1): #Start time
                startTimeList.append(tableStart[:tableStart.find("<br>")].replace(" ",""))
                tableStart = tableStart[tableStart.find("<br>")+4:]
            print("Start time"+startTimeList[0])
            table = table[table.find("</td>")+4:]
            tableEnd = table[:table.find("</td>")]

            while (tableEnd.find("<br>")!= -1): #End time
                endTimeList.append(tableEnd[:tableEnd.find("<br>")].replace(" ",""))
                tableEnd = tableEnd[tableEnd.find("<br>")+4:]
            table = table[table.find("floor map for")+13:]
            tableRoom = table[:table.find("/td")]

            while (tableRoom.find("</a>") != -1):  # Start time
                roomList.append(tableRoom[tableRoom.find(">")+1:tableRoom.find("</a>")])
                tableRoom = tableRoom[tableRoom.find("floor map for") + 13:]
                print(roomList)
            lectureDic["instructorlist"]=instructorList
            lectureDic["startTimeList"] = startTimeList
            lectureDic["endTimeList"] = endTimeList
            lectureDic["roomList"] = roomList
            lectureDic["tableDayList"] = tableDayList
            lstofDic.append(lectureDic)

HTMLParser("asd")