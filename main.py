import discord
import os
import Botv2
from replit import db
from keep_alive import keep_alive
import asyncio
import pytz
import datetime
import api

token = os.environ['TOKEN']
client = discord.Client()

async def loop():
  counter = 1
  while True:
    est = pytz.timezone('US/Eastern')
    now = datetime.datetime.now().astimezone(est)
    current_time = now.strftime("%H")
    database = db["database"]
    if api.connect_check() == 0:
      # connected
      if api.status_check() == 1:
        # checks if theres school
        print("no school")
        # make counter 0 so if it's 7 on a school day it can run
        counter = 0
      elif api.status_check() == 0:
        # if theres school
        if current_time == "07":
          # if it's 7am
          if counter == 0:
            # if its ready
            total_time = Botv2.execute(database)
            channel = client.get_channel(428729686185476097)
            await channel.send("Rise and Shine! It's 7 AM!\n" + "Total Run Time: " + str(total_time) + " Seconds.")
            # counter = 1 to make it on cool down
            counter = 1
            print("running")
          else:
            # it's still 7am and it's counter = 1
            print("on cool down")
        else:
          # it's no longer 7am and now counter is 0, it's ready to go once time hits 7 again.
          counter = 0
          print("condition not met")

    elif api.connect_check() == 111:
      # if api doesn't work
      await channel.send("<@249632647473659904> API IS DOWN!!!")
      # force shutdown
      exit()

    # checking for counting.
    if counter == 0:
      await asyncio.sleep(30)
      print("ready")
    if counter == 1:
      await asyncio.sleep(30)
      print("not ready")

def update_add(fname, lname, email, school):
  if "database" in db.keys():
    database = db["database"]
    data = [fname, lname, email, school]
    database.append(data)
    db["database"] = database
  else:
    database = []
    data = [fname, lname, email, school]
    db["database"] = data

def update_del(index):
  database = db["database"]
  if len(database) > index:
    del database[index]
    db["database"] = database
    return 0
  else:
    return 1


@client.event
async def on_ready():
  activity = discord.Game(name="$help", type=3)
  await client.change_presence(status=discord.Status.idle, activity=activity)

  print("We have logged in as {0.user}"
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith("$whoami"):
    await message.channel.send("You are " + str(message.author))
  
  if msg.startswith("$help"):
    await message.channel.send("Commands\n\n$whoami | check your discord tag\n\n$append Firstname Lastname Email School | add yourself to the list\n\nList of schools:\nsiths\nndhs\n\n$remove index_number | remove yourself from the list, list starts at number 1\n\n$clear | clear the list *caution*\n\n$show | show the list\n\n$sysshow | show the list system like\n\n$FORCESTOP | Shutdown Bot in case of error")

  if msg.startswith("$run"):
    await message.channel.send("Running...")
    database = db["database"]
    total_time = Botv2.execute(database)
    await message.channel.send("Finished!\nTotal Run Time: " + str(total_time) + " Seconds")

  if msg.startswith("$append"):
    fname = msg.split()[1]
    lname = msg.split()[2]
    email = msg.split()[3]
    school = msg.split()[4]
    update_add(fname, lname, email, school)
    database = db["database"]
    await message.channel.send(fname.capitalize() + " has been added!\nuse $show to see full list")

  if msg.startswith("$remove"):
    database = db["database"]
    if "database" in db.keys():
      index = int(msg.split()[1])
      if update_del((index - 1)) == 0:
        await message.channel.send(database[index-1][0].capitalize() + " has been removed!\nuse $show to see full list")
      elif update_del((index - 1)) == 1:
        await message.channel.send("Index_Number is greater than the list. Try again.")

  if msg.startswith("$clear"):
    db.clear()
    database = []
    db["database"] = database
    database = db["database"]
    await message.channel.send("Cleared!\nuse $show to see full list")

  if msg.startswith("$show"):
    database = db["database"]
    await message.channel.send("Here's the list!")
    for i in range(len(database)):
      num = i + 1
      await message.channel.send(str(num) + ". " + database[i][0].capitalize() + " " + database[i][1].capitalize() + ", " + database[i][2] + ", " + database[i][3])

  if msg.startswith("$sysshow"):
    database = db["database"]
    await message.channel.send(str(database))
  
  if msg.startswith("$FORCESTOP"):
    await message.channel.send("<@249632647473659904> Going offline")
    print("shutdown")
    exit()
      
keep_alive()
client.loop.create_task(loop())
client.run(token)