web = __import__('webScraper')

lst = web.HTMLParser()
for i in lst:
    web.clean_distribution(i)
    web.clean_prereq(i)

test = lst[6]
test2 = lst
#for i in lst:
#    clean_distribution(i)
#print(lst)

#print(test['prereq'])
#print(test['course name'])
def recognized_prereq(lst): #Return a list of all the courses with a recognizable coursecode
    recognized = []
    recognized_dict= {}
    for dict in lst:
        if "prereq" not in dict:
            pass
        else:
            print(dict['prereq'])
            prereq = dict['prereq']
            prereq = prereq.replace('(',"").replace(' ',"").replace("/",",").replace(")","").replace(";",",")
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
def interface(recognized_dict):
    courseStructure = ""
    for key in recognized_dict:
        courseStructure= key
        for i in recognized_dict[key]:
            courseStructure+="---->"+i+"\n"+"        "
        print(courseStructure)


dict = (recognized_prereq(test2))
interface(dict)