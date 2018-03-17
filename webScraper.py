import requests
import json
from pymongo import MongoClient
# from bs4 import BeautifulSoup
rec_prereq = __import__('prerequisite')
client = MongoClient('localhost', 27017)
db = client.test
collection = db.courses

prereq = db.prereq

class HTMLParser():
    def __init__(self):
        self.recognized_dict={}
        collection.drop()
        self.startParser()

    def startParser(self):
        for i in range(80):
            lst = self.HTMLParser(str(i))
            self.recognized_dict = rec_prereq.recognized_prereq(lst,self.recognized_dict)
        # lst = self.HTMLParser(str(9))
        # self.recognized_dict = rec_prereq.recognized_prereq(lst,self.recognized_dict)
        # print(self.recognized_dict)
        prereq.insert(self.recognized_dict)
        print("done \n")

    def HTMLParser(self, program):
        raw_text = requests.get("http://student.utm.utoronto.ca/calendar/list_courses.pl?Depart="+program)
        text =  raw_text.content.decode("utf-8")
        text = text[text.find("Academic Calendar 2017"):]#we cut text to make the file shorter
        if text.find("Program Not Found") != -1 or text.find("This program is no longer offered")!=-1 or text.find("Department Not Found")!= -1:
            # print("this runs")
            return []
        else:
            return self.get_date(text)

    def get_date(self, text):
        lst = []
        while text.find('p class="titlestyle"')!=-1:
            current_course_dict = {}

            length = text.find("titlestyle")+len("titlestyle'>")
            courseCode = text[length:length+8]
            current_course_dict["course code"]= courseCode

            courseName = text[length+8:text.find("<span")]
            current_course_dict["course name"]= courseName

            distLength = text.find("abbr title")+len("abbr title='")
            distEnd = text.find("</abbr")
            distribution = text[distLength:distEnd]
            current_course_dict["distribution"] = distribution


            text= text[distEnd:]
            fullText = text[text.find('p class="titlestyle"'):]
            nextCourseLen = text.find('p class="titlestyle"')
            text=text[:nextCourseLen] #we split each course now
            # course description
            descriptionLen = text.find("normaltext")+len("normaltext'>")+1
            if (text.find("Helpcourse")==-1):
                textLength = text.find("<br>")
                courseDescription=text[descriptionLen:textLength]
                courseDescription=self.clean_description(courseDescription)
                current_course_dict["course description"] = courseDescription
                text= text[textLength+4:]
            else:
                textLength = text.find("<abbr")-2
                courseDescription=text[descriptionLen:textLength]
                courseDescription=self.clean_description(courseDescription)
                current_course_dict["course description"] = courseDescription
                text=text[textLength+5:]



            if text.find("Exclusion")!=-1:
                exclusionLength = text.find("</span>")+7
                exText = text[exclusionLength:]
                exclusionEnd = exText.find("<br>")
                rawExclusion=exText[:exclusionEnd]
                current_course_dict["exclusion"] = rawExclusion
                text = text[exclusionEnd+4:]

            findPrerequisite = text.find("Prerequisite")

            if findPrerequisite!=-1:
                prereqLength = findPrerequisite+21 #length of </span> and prerequisite
                preText = text[prereqLength:]
                preReqEnd = preText.find("<br>")
                rawPrereq = preText[:preReqEnd]
                rawPrereq=self.cleanPrereq(rawPrereq)
                current_course_dict["prereq"] = rawPrereq
                text =text[preReqEnd+4:]

            CoreRequisite = text.find("Corequisite:")

            if CoreRequisite!=-1:
                coreLen= CoreRequisite+20
                coreText = text[coreLen:]
                coreEnd= coreText.find("<br>")
                rawCore = coreText[:coreEnd]
                current_course_dict["corequisite"] = rawCore
                text=text[coreEnd+4:]

            text = fullText
            self.clean_distribution(current_course_dict)
            self.clean_prereq(current_course_dict)
            self.clean_coreq(current_course_dict)
            lst.append(current_course_dict)
            collection.insert(current_course_dict)
        return lst

    def clean_distribution(self, dict):
        raw_course_name= dict['distribution']
        end = raw_course_name.find(">")-1
        if end==-2:
            pass
        else:
            dict['distribution'] = raw_course_name[:end]

    def clean_prereq(self, dict):
        if "prereq" not in dict:
            return dict
        raw_prereq = dict["prereq"]
        prereq = ""
        js = raw_prereq.find("<a")
        while js!=-1:
            course_beg = raw_prereq.find("Course=")+7
            course_end = raw_prereq.find("</a>")+4
            raw_prereq = raw_prereq[:js]+raw_prereq[course_beg:+course_beg+8]+raw_prereq[course_end:]
            js = raw_prereq.find("<a")
        dict['prereq'] = raw_prereq

    def clean_coreq(self, dict):
        if "corequisite" not in dict:
            return dict
        raw_coreq = dict["corequisite"]
        corequisite = ""
        js = raw_coreq.find("<a")
        while js!=-1:
            course_beg = raw_coreq.find("Course=")+7
            course_end = raw_coreq.find("</a>")+4
            raw_coreq = raw_coreq[:js]+raw_coreq[course_beg:+course_beg+8]+raw_coreq[course_end:]
            js = raw_coreq.find("<a")
        dict['corequisite'] = raw_coreq

    def clean_description(self, description):
        dest = description
        while(dest.find("<br />")!=-1):
            dest = dest.replace("<br />","")
        while(dest.find("<a href")!=-1):
            atag = dest.find("<a href")
            exText = dest[:atag]
            leftover= dest[atag:]
            datastart = leftover.find('">')+2
            endofatag = leftover.find("</a>")
            data=leftover[datastart:endofatag]
            endofatag = endofatag +4
            rest = leftover[endofatag+4:]
            dest=exText + data + rest
        while(dest.find("<a target=")!=-1):
            atag = dest.find("<a target=")
            exText = dest[:atag]
            leftover= dest[atag:]
            datastart = leftover.find('>')+1
            endofatag = leftover.find("</a>")
            data=leftover[datastart:endofatag]
            leftover = leftover[endofatag+4:]
            dest=exText + data + leftover
        return dest

    def cleanPrereq(self, description):
        dest = description
        while(dest.find("<br />")!=-1):
            dest = dest.replace("<br />","")
        while(dest.find("<a href")!=-1):
            atag = dest.find("<a href")
            exText = dest[:atag]
            leftover=dest[atag:]
            datastart = leftover.find('">')+2
            endofatag = leftover.find("</a>")
            data=leftover[datastart:endofatag]
            leftover = leftover[endofatag+4:]
            dest=exText + data + leftover

        while(dest.find("<span")!=-1):
            stag = dest.find("<span")
            exText = dest[:stag]
            datastart = dest[stag:].find('>')+1
            endofatag = dest[stag:].find("</span>")
            leftover=dest[stag:]
            data=leftover[datastart:endofatag]
            leftover=leftover[endofatag+7:]
            dest=exText+data+leftover
        return dest


if __name__ == '__main__':
    scraper = HTMLParser()
