# Using NYC 311 Public Developers api key to check if school is opened
import os
import requests
import json
from checking_time import check_day

KEY = os.environ['APIKEY']
m, d, y = check_day()
adate = "{}/{}/{}".format(m, d, y)
bdate = "{}/{}/{}".format(m, d, y)
print(adate)
r = requests.get("https://api.nyc.gov/public/api/GetCalendar?fromdate={}&todate={}".format(adate, bdate), headers={"Ocp-Apim-Subscription-Key": KEY})

data = json.loads(r.text)
status = data["days"][0]["items"][2]["status"]
reason = data["days"][0]["items"][2]["details"]

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

