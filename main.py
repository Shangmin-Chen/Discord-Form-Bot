import discord
import os
import Botv2
from replit import db
from keep_alive import keep_alive
import asyncio
from checking_time import check_six
import api

token = os.environ['TOKEN']
client = discord.Client()

async def loop():
  # Giving time for the bot to connect.
  while client.get_channel(428729686185476097) == None:
    await asyncio.sleep(1)
    if client.get_channel(428729686185476097) != None:
      channel = client.get_channel(428729686185476097)
      print(channel)
      break
  # Constant or init variables
  cool_down = 0
  while True:
    try:
      database = db["database"]
    except:
      await channel.send("<@249632647473659904> Database Error")
      exit()
    if check_six() == 0:
      # it's 6
      if cool_down == 0:
        # init run
        value, reason, vdate = api.run_api()
        if value == 1:
          # checks if theres school
          await channel.send("Today is {}, {}, No school: {}".format(vdate, reason))
          # make it go on cooldown
          cool_down = 1
        elif value == 0:
          total_time = Botv2.execute(database)
          await channel.send("Time for school, today is {}, {}\n Total Run Time: {} seconds".format(vdate, str(total_time)))
          # make it go on cooldown
          cool_down = 1
        elif value == 111:
          # request failed
          # api doesn't work, didn't connect
          await channel.send("<@249632647473659904> API IS DOWN")
          # force shutdown
          exit()
    else:
      print("not 6")

    if cool_down == 0:
      print("ready")
      await asyncio.sleep(60)
    elif cool_down == 1:
      if check_six() == 1:
        # this makes sure that the code runs once at 6, and goes into cooldown. Once it's not 6, it goes off cooldown and becomes available again.
        cool_down = 0
        print("no longer 6")
        await asyncio.sleep(60)
      else:
        print("not ready")
        await asyncio.sleep(60)


# defining algorithm
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

# checking connection
@client.event
async def on_ready():
  activity = discord.Game(name="$help", type=3)
  await client.change_presence(status=discord.Status.idle, activity=activity)

  print("We have logged in as {0.user}"
  .format(client))

# defining events functions when bot command is called
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith("$whoami"):
    await message.channel.send("You are " + str(message.author))
  
  if msg.startswith("$help"):
    await message.channel.send("\nCommands\n\n$whoami | check your discord tag\n\n$append Firstname Lastname Email School | add yourself to the list\n\nList of schools:\nsiths\nndhs\n\n$remove index_number | remove yourself from the list, list starts at number 1\n\n$clear | clear the list *caution*\n\n$show | show the list\n\n$sysshow | show the list system like\n\n$FORCESTOP | Shutdown Bot in case of error")

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
    organized_list = []
    for i in range(len(database)):
      num = i + 1
      msg = str(num) + ". " + database[i][0].capitalize() + " " + database[i][1].capitalize() + ", " + database[i][2] + ", " + database[i][3]
      organized_list.append(msg)
    await message.channel.send("Here's the list!\n" + ("\n".join(organized_list)))

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
