from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.test
collection = db.courses

def recognized_prereq(lst,recognized_dict): #Return a dictionary of all the courses with a recognizable coursecode
    recognized = []
    prereqs_actual=[]
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

                # time.sleep(0.5)
                if len(i)==8:
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    prefix=i[:3]
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['course code'])
                    else:
                        recognized_dict[i] = [dict['course code']]
                elif len(i) ==4 or len(i) ==5:
                    i = prefix+i
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    recognized.append(i)
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['course code'])
                    else:
                        recognized_dict[i] = [dict['course code']]

        if len(prereqs_actual)>0:
            collection.update_one({"course code":dict["course code"]}, {'$set': {"prerequisites":prereqs_actual}})
            prereqs_actual=[]
        else:
            collection.update_one({"course code":dict["course code"]}, {'$set': {"prerequisites":None}})
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
