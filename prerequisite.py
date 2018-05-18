#web = __import__('webScraper')
#from pymongo import MongoClient
#for i in lst:
#    clean_distribution(i)
#print(lst)
import time

# Wait for 5 seconds

#print(test['prereq'])
#print(test['course name'])
def recognized_prereq(lst,recognized_dict): #Return a dictionary of all the courses with a recognizable coursecode
    recognized = []
    for dict in lst:
        if "prereq" not in dict: #{Course code:mat223,prereq:CSC108,MAT102}
            pass
        else:
            prereq = dict['prereq']
            prereq = prereq.replace('(',"").replace("/",",").replace(")","").replace(";",",").replace("."," dot ")
            prereq_lst = prereq.split(',')

            prefix =''

            prereq_lst = clean(prereq_lst)
            # print(prereq_lst)
            for i in prereq_lst:
                if(i=="351H5"):
                    print(prereq_lst)
                # time.sleep(0.5)
                if len(i)==8:
                    #recognized.append(i)
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
#def getCourseInfo(courseCode,collection): #DB Search for courses that have a specific prerequisite
        #calls database to grab Courseinfo
#    return collection.find_one({"course code":courseCode})
def clean(lst):
    new_lst=[]
    for i in lst:
        x=i.find("Y5")
        if(x==-1):
            x=i.find("H5")
        if(x!=-1):
            new_lst.append(i[x-6:x+2])
    return new_lst



def grabSearch(searchParameter):
    #call db function that searches for prereq
    #returns object and return as JS object
    pass
