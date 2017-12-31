import requests
import pyjs

def HTMLParser(courseName):
    raw_text = requests.get("http://student.utm.utoronto.ca/calendar/list_courses.pl?Depart=7")
    text =  raw_text.content.decode("utf-8")
    text = text[text.find("Academic Calendar 2017"):]#we cut text to make the file shorter
    lst = []
    while text.find('p class="titlestyle"')!=-1:
        dict = {}

        length = text.find("titlestyle")+len("titlestyle'>")
        courseCode = text[length:length+8]
        dict["course code"]= courseCode

        courseName = text[length+8:text.find("<span")]
        dict["course name"]= courseName

        distLength = text.find("abbr title")+len("abbr title='")
        distEnd = text.find("</abbr")
        distribution = text[distLength:distEnd]
        dict["distribution"] = distribution

        text= text[distEnd:]
        fullText = text[text.find('p class="titlestyle"'):]
        nextCourseLen = text.find('p class="titlestyle"')
        text=text[:nextCourseLen] #we split each course now


        descriptionLen = text.find("normaltext")+len("normaltext'>")+1
        if (text.find("Helpcourse")==-1):
            textLength = text.find("<br>")
            courseDescription=text[descriptionLen:textLength]
            dict["course description"] = courseDescription
            text= text[textLength+4:]
        else:
            textLength = text.find("<abbr")-2
            courseDescription=text[descriptionLen:textLength]
            dict["course description"] = courseDescription
            text=text[textLength+5:]

        if text.find("Exclusion")!=-1:
            exclusionLength = text.find("</span>")+7
            exText = text[exclusionLength:]
            exclusionEnd = exText.find("<br>")
            rawExclusion=exText[:exclusionEnd]
            dict["exclusion"] = rawExclusion
            text = text[exclusionEnd+4:]

        if text.find("Prerequisite")!=-1:
            #print(text)
            prereqLength = text.find("Prerequisite")+19 #length of </span> and prerequisite
            preText = text[prereqLength:]
            preReqEnd = preText.find("<br>")
            rawPrereq = preText[:preReqEnd]
            #print(rawPrereq)
            dict["prereq"] = rawPrereq
            text =text[preReqEnd+4:]

        findCoreRequisite = text.find("Corerequisite:")
        if findCoreRequisite!=-1:
            coreEnd= text.find("<br>")
            coreLen= findCoreRequisite+20
            rawCore = text[coreLen:coreEnd]
            dict["core"] = rawCore
            text=text[coreEnd+4:]
        text = fullText
        print(dict)
        lst.append(dict)
        #print(dict)
    return lst
print(HTMLParser("asd"))