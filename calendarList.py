import datetime
from setup import getCalendarService

def calendarList():
    service = getCalendarService()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=40,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get  ('items',[])
    
    return events
    
    # if not events:
    #    print('No upcoming events found.')
    # for event in events:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])



calendarList()

