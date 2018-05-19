import requests
import json
import time
# Wait for 5 seconds
tree_node = __import__('tree')
from pymongo import MongoClient
# from bs4 import BeautifulSoup
rec_prereq = __import__('prerequisite')
client = MongoClient('localhost', 27017)
db = client.test
collection = db.courses



def flow(course): #course ia string ex: CSC148
    data = collection.find_one({"course code":course}) #data is a dictionary containing course info
    tree = tree_node.make_tree(data['course code']) #make a tree node
    dict = {}
    dict[data["course code"]] = tree
    flow_chart = flow_helper(tree,dict,data)
def flow_helper(tree,dict,data):
    if data["prereq"]:
        for i in data["prerequisites"]:
            course = collection.find_one({"course code": i})
            if not dict[i]:

                node = tree_node.make_tree(course['course code'])
                dict[i] = node
                tree.prev.append(node)
            else:
                if dict[i]:
                    tree.prev.append(dict[i])
            flow_helper(tree.prev,dict,i)
    if data["required_for"]:
        for i in data["required_for"]:
            course = collection.find_one({"course code": i})
            node = tree_node.make_tree(course['course code'])
            dict[i] = node
            tree.next.append(node)
        else:
            if dict[i]:
                tree.next.append(dict[i])
        flow_helper(tree.next, dict, i)