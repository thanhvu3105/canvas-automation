from setup import getCalendarService
from calendarList import calendarList
from datetime import datetime, timedelta,timezone
import json
import pprint


def addEvent():
    service = getCalendarService()
    eventList = calendarList()

    


    #get current date
    currentDate = datetime.now().date()

    with open("assignmentsDue.json",'r') as f:
        data = json.load(f)
    
    now = datetime.now().date()


    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=1)).isoformat()


    for course,items in data.items():
        for item in items:
            if(item[2] != None):
                # start = datetime.now().date()
                d = datetime.strptime(item[2],"%Y-%m-%dT%H:%M:%SZ")
                deadline = datetime(d.year,d.month,d.day,d.hour,d.minute,d.second)
                start = (deadline - timedelta(hours=10)).isoformat()
                end = (deadline - timedelta(hours=5)).isoformat()
               

                event_result = service.events().insert(calendarId='primary',
                    body={
                        "summary": str(course),
                        "description": str(item[1]),
                        "start":{"dateTime" : start, "timeZone": "America/Chicago"},
                        "end" : {"dateTime" : end , "timeZone": "America/Chicago"},
                        }
                    ).execute()

         
    f.close()  


addEvent()



