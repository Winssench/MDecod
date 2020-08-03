import datetime
timeStamp = "2020-07-29T13:04:19.1130000Z"
timeStamp = timeStamp.split('.')[0]
timeStamp = timeStamp.replace('T', ' ')
print("here", timeStamp)

presentTime = datetime.datetime.utcnow()
#>>> datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
print(presentTime)
#print(presentTime.strftime('%m %d %Y - %H:%M:%S'))
print(presentTime.strftime('%Y-%m-%dT%H:%M:%SZ'))
