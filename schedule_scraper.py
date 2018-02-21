import requests
def HTMLParser(course): #course is a list
    course = ["CSC108"]
    raw_text = "https://student.utm.utoronto.ca/timetable/timetable?yos=&subjectarea=&session=20179&courseCode=CSC108H5&sname=&delivery=&courseTitle="
    text = raw_text.content.decode("utf-8")
    for i in course:
        text = text[text.find(i):]  # we cut text to make the file shorter
        text = text[text.find("h4")+3:]
        coursename= text[:text.find("h4")]

        table = text[text.find("tbl_"+i):]
        table = text[text.find(i):]
