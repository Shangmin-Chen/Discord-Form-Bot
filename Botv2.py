import requests
from time import time
url = "https://healthscreening.schools.nyc/home/submit"

def RUN(email, fname, lname, school):
    data = {
        "Type": "G",
        "IsOther": "False",
        "IsStudent": "1",
        "FirstName": fname,
        "LastName": lname,
        "Email": email,
        "State": "NY",
        "Location": school,
        "Floor": "",
        "Answer1": "0",
        "Answer2": "0",
        "Answer3": "0",
        "ConsentType": "",
    }

    response = requests.post(url, data=data).text
    print(response)

def execute(list):
  total_run_time = 0
  for i in range(len(list)):
    start = time()
    if list[i][3] == "siths".lower():
      school = "R605"
    if list[i][3] == "ndhs".lower():
      school = "R440"
    RUN(list[i][2], list[i][0].capitalize(), list[i][1].capitalize(), school)
    end = time()
    seconds = (end - start)
    total_run_time += seconds
  return total_run_time.__round__(5)

