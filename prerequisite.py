#web = __import__('webScraper')
from pymongo import MongoClient
#for i in lst:
#    clean_distribution(i)
#print(lst)

#print(test['prereq'])
#print(test['course name'])
def recognized_prereq(lst): #Return a dictionary of all the courses with a recognizable coursecode
    recognized = []
    recognized_dict= {}
    for dict in lst:
        if "prereq" not in dict:
            pass
        else:
            prereq = dict['prereq']
            prereq = prereq.replace('(',"").replace(' ',"").replace("/",",").replace(")","").replace(";",",").replace("."," dot ")
            prereq_lst = prereq.split(',')
            prefix =''
            for i in prereq_lst:
                if len(i)==8:
                    recognized.append(i)
                    prefix=i[:3]
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['course code'])
                    else:
                        recognized_dict[i] = [dict['course code']]
                elif len(i) ==4 or len(i) ==5:
                    i = prefix+i
                    recognized.append(i)
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['course code'])
                    else:
                        recognized_dict[i] = [dict['course code']]

    return recognized_dict
def getCourseInfo(courseCode,collection): #DB Search for courses that have a specific prerequisite
        #calls database to grab Courseinfo
    return collection.find_one({"course code":courseCode})

def grabSearch(searchParameter):
    #call db function that searches for prereq
    #returns object and return as JS object
    pass