import requests
import os
from dotenv import load_dotenv
import json
import pprint
from datetime import datetime

load_dotenv()
key = os.getenv('TOKEN_KEY')


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):  
        r.headers["authorization"] = "Bearer " + self.token
        return r

#get user ID
def getUserID(endpoint):
    userInfo = requests.get(endpoint + "/users/self",auth=BearerAuth(key))
    userId = userInfo.json()["id"]
    return userId


#get course ID 
def getCourseID(endpoint,userId):
    courseID = [] 
    payload = {'enrollment_state' : 'active'}
    courseInfo = requests.get(endpoint + f"/courses",params=payload, auth=BearerAuth(key))
    courseInfo = courseInfo.json()
    
    for data in courseInfo:
        if 'name' in data:
            courseID.append([data['name'],data['id']])
        else:
            continue
    return courseID


#get assignments
def getAssignments(endpoint,courseID):    
    pp = pprint.PrettyPrinter(indent=4)

    assignmentsInfo = []
    payload = { 'bucket':'future', 'order_by':'due_at','include[]':'overrides'}
    assignments = requests.get(endpoint + f"/courses/{courseID}/assignments",params=payload ,auth=BearerAuth(key))
    assignments = assignments.json()
    # for i in assignments:
        # print(i['name'] , " DUE DATE: " , i['due_at'])

    for i in range(0,len(assignments)):
        # print(assignments[i]['id'],assignments[i]['name'],assignments[i]['due_at'])
        if(assignments[i]['due_at'] != None):
            assignmentsInfo.append([assignments[i]['id'],assignments[i]['name'],assignments[i]['due_at']])
    return assignmentsInfo


#Assignments deadlines 
def exportJSON():
    endpoint = "https://canvas.txstate.edu/api/v1"
    userID = getUserID(endpoint)
    courseID = getCourseID(endpoint,userID)
    assignmentsInfo = {}


    for course in courseID:
        # getAssignments(endpoint,course[1])
        assignmentsInfo[course[0]] = getAssignments(endpoint,course[1])

    outData = json.dumps(assignmentsInfo,indent=4)

    with open("assignmentsDue.json","w") as outfile:
        outfile.write(outData)
        
    # print(assignmentsInfo)

    
# if __name__ == "__main__":
#     main()  