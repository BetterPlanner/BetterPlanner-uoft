import requests
import pyjs
import json
def HTMLParser():
    raw_text = requests.get("http://student.utm.utoronto.ca/calendar/list_courses.pl?Depart=9")
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
        findPrerequisite = text.find("Prerequisite")
        if findPrerequisite!=-1:
            #print(text)
            prereqLength = findPrerequisite+21 #length of </span> and prerequisite
            preText = text[prereqLength:]
            preReqEnd = preText.find("<br>")
            rawPrereq = preText[:preReqEnd]
            #print(rawPrereq)
            dict["prereq"] = rawPrereq
            text =text[preReqEnd+4:]

        findCoreRequisite = text.find("Corequisite:")
        if findCoreRequisite!=-1:

            coreLen= findCoreRequisite+20
            coreText = text[coreLen:]
            coreEnd= coreText.find("<br>")
            rawCore = coreText[:coreEnd]
            dict["corequisite"] = rawCore
            text=text[coreEnd+4:]
        text = fullText
        #print(dict)
        lst.append(dict)
        #print(dict)
    #with open('file.txt', 'w') as file: #This will write the lst of dictionaries into a file, will soon be replaced with a DB
        #for i in lst:
            #file.write(json.dumps(i))
    return lst


def clean_distribution(dict):
    raw_course_name= dict['distribution']
    end = raw_course_name.find(">")-1
    dict['distribution'] = raw_course_name[:end]

def clean_prereq(dict):
    if "prereq" not in dict:
        return dict
    raw_prereq = dict["prereq"]
    prereq = ""
    js = raw_prereq.find("<a")
    while js!=-1:
        course_beg = raw_prereq.find("Course=")+7
        #print(course_beg)
        course_end = raw_prereq.find("</a>")+4
        raw_prereq = raw_prereq[:js]+raw_prereq[course_beg:+course_beg+8]+raw_prereq[course_end:]
        #print(raw_prereq)
        js = raw_prereq.find("<a")
        #print(js)
    dict['prereq'] = raw_prereq


#lst = HTMLParser()
#test = lst[33]
#for i in lst:
#    clean_distribution(i)
#print(lst)
#clean_prereq(test)
#print(test['prereq'])
#print(test['course name'])