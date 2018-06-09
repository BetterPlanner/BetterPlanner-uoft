from pymongo import MongoClient
client = MongoClient('localhost', 27017)

test_db        = client.test

utm_courses     = test_db.utm_courses
utsc_courses    = test_db.utsc_courses
utsg_courses    = test_db.utsg_courses

def recognized_prereq_utsg(lst,recognized_dict): #Return a dictionary of all the courses with a recognizable coursecode
    recognized = []
    prereqs_actual=[]
    for dict in lst:
        if "prerequisites" not in dict: #{Course code:mat223,prereq:CSC108,MAT102}
            pass
        else:
            prereq = dict['prerequisites']
            prereq = prereq.replace('(',"").replace("/",",").replace(")","").replace(";",",").replace("."," dot ")
            prereq_lst = prereq.split(',')

            prefix =''

            prereq_lst = clean(prereq_lst,"1")
            # print(prereq_lst)

            for i in prereq_lst:

                # time.sleep(0.5)
                if len(i)==8:
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    prefix=i[:3]
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['code'])
                    else:
                        recognized_dict[i] = [dict['code']]
                elif len(i) ==4 or len(i) ==5:
                    i = prefix+i
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    recognized.append(i)
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['code'])
                    else:
                        recognized_dict[i] = [dict['code']]

        if len(prereqs_actual)>0:
            utsg_courses.update_one({"code":dict["code"]}, {'$set': {"prerequisites_array":prereqs_actual}})
            prereqs_actual=[]
        else:
            utsg_courses.update_one({"code":dict["code"]}, {'$set': {"prerequisites_array":None}})
    return recognized_dict

def recognized_prereq_utsc(lst,recognized_dict): #Return a dictionary of all the courses with a recognizable coursecode
    recognized = []
    prereqs_actual=[]
    for dict in lst:
        if "prerequisites" not in dict: #{Course code:mat223,prereq:CSC108,MAT102}
            pass
        else:
            prereq = dict['prerequisites']
            prereq = prereq.replace('(',"").replace("/",",").replace(")","").replace(";",",").replace("."," dot ")
            prereq_lst = prereq.split(',')

            prefix =''

            prereq_lst = clean(prereq_lst,"3")
            # print(prereq_lst)

            for i in prereq_lst:

                # time.sleep(0.5)
                if len(i)==8:
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    prefix=i[:3]
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['code'])
                    else:
                        recognized_dict[i] = [dict['code']]
                elif len(i) ==4 or len(i) ==5:
                    i = prefix+i
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    recognized.append(i)
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['code'])
                    else:
                        recognized_dict[i] = [dict['code']]

        if len(prereqs_actual)>0:
            utsc_courses.update_one({"code":dict["code"]}, {'$set': {"prerequisites_array":prereqs_actual}})
            prereqs_actual=[]
        else:
            utsc_courses.update_one({"code":dict["code"]}, {'$set': {"prerequisites_array":None}})
    return recognized_dict


def recognized_prereq_utm(lst,recognized_dict): #Return a dictionary of all the courses with a recognizable coursecode
    recognized = []
    prereqs_actual=[]
    for dict in lst:
        if "prerequisites" not in dict: #{Course code:mat223,prereq:CSC108,MAT102}
            pass
        else:
            prereq = dict['prerequisites']
            prereq = prereq.replace('(',"").replace("/",",").replace(")","").replace(";",",").replace("."," dot ")
            prereq_lst = prereq.split(',')

            prefix =''

            prereq_lst = clean(prereq_lst,"5")
            # print(prereq_lst)

            for i in prereq_lst:

                # time.sleep(0.5)
                if len(i)==8:
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    prefix=i[:3]
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['code'])
                    else:
                        recognized_dict[i] = [dict['code']]
                elif len(i) ==4 or len(i) ==5:
                    i = prefix+i
                    if i not in prereqs_actual:
                        prereqs_actual.append(i)
                    recognized.append(i)
                    if i in recognized_dict:
                        recognized_dict[i].append(dict['code'])
                    else:
                        recognized_dict[i] = [dict['code']]

        if len(prereqs_actual)>0:
            utm_courses.update_one({"code":dict["code"]}, {'$set': {"prerequisites_array":prereqs_actual}})
            prereqs_actual=[]
        else:
            utm_courses.update_one({"code":dict["code"]}, {'$set': {"prerequisites_array":None}})
    return recognized_dict

def clean(lst,campus):
    new_lst=[]
    for i in lst:
        x=i.find("Y"+campus)
        if(x==-1):
            x=i.find("H"+campus)
        if(x!=-1):
            new_lst.append(i[x-6:x+2])
    return new_lst
