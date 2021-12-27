import pytz
import datetime

est = pytz.timezone('US/Eastern')
now = datetime.datetime.now().astimezone(est)

d = now.strftime("%d")
m = now.strftime("%m")
y = now.strftime("%Y")
current_time = now.strftime("%H")

def check_seven():
  if current_time == "07":
    return 0
  else:
    return 1