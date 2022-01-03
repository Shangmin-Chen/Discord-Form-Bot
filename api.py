# Using NYC 311 Public Developers api key to check if school is opened
import os
import requests
import json
from checking_time import check_day

KEY = os.environ['APIKEY']

def run_api():
  m, d, y = check_day()
  vdate = "{}/{}/{}".format(m, d, y)
  r = requests.get("https://api.nyc.gov/public/api/GetCalendar?fromdate={}&todate={}".format(vdate, vdate), headers={"Ocp-Apim-Subscription-Key": KEY})

  data = json.loads(r.text)
  status = data["days"][0]["items"][2]["status"]
  reason = data["days"][0]["items"][2]["details"]

  if r.status_code == 200:
    # connected/ good
    if status == "NOT IN SESSION" or status == "CLOSED":
    # closed/ false
      return 1, reason, vdate
    else:
      # school in session/ true
      return 0, reason, vdate
  else:
    # not connected/ very bad
    return 111

  

