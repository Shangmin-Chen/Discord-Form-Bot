import requests
from time import perf_counter
import threading

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

def execute(data_list):
  start = perf_counter()
  length = len(data_list)
  def do_task(fname, lname, email, school):
    if school == "siths".lower():
      school = "R605"
    elif school == "ndhs".lower():
      school = "R440"
    RUN(email, fname.capitalize(), lname.capitalize(), school)
  
  threads = []

  for i in range(length):
    fname = data_list[i][0]
    lname = data_list[i][1]
    email = data_list[i][2]
    school = data_list[i][3]
    t = threading.Thread(target=do_task, daemon=True, args=(fname, lname, email, school))
    threads.append(t)

  for i in range(length):
    threads[i].start()
  
  for i in range(length):
    threads[i].join()

  end = perf_counter()
  total_run_time = end - start
  return total_run_time.__round__(5)