import pytz
import datetime

def check_seven():
  est = pytz.timezone('US/Eastern')
  now = datetime.datetime.now().astimezone(est)

  current_time = now.strftime("%H")
  if current_time == "07":
    return 0
  else:
    return 1

def check_day():
  est = pytz.timezone('US/Eastern')
  now = datetime.datetime.now().astimezone(est)

  d = now.strftime("%d")
  m = now.strftime("%m")
  y = now.strftime("%Y")

  return m, d, y
