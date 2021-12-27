# Using NYC 311 Public Developers api key to check if school is opened
import os
import requests
import json
import pytz
import datetime

est = pytz.timezone('US/Eastern')
now = datetime.datetime.now().astimezone(est)
d = now.strftime("%d")
m = now.strftime("%m")
y = now.strftime("%Y")


KEY = os.environ['APIKEY']
adate = "{}/{}/{}".format(m,d,y)
bdate = "{}/{}/{}".format(m,d,y)

r = requests.get("https://api.nyc.gov/public/api/GetCalendar?fromdate={}&todate={}".format(adate, bdate), headers={"Ocp-Apim-Subscription-Key": KEY})

data = json.loads(r.text)
status = data["days"][0]["items"][2]["status"]

def connect_check():
  if r.status_code == 200:
    # connected/ good
    return 0 
  else:
    # not connected/ very bad
    return 111

def status_check():
  if status == "NOT IN SESSION" or status == "CLOSED":
    # closed/ bad
    return 1
  else:
    # school in session/ good
    return 0

