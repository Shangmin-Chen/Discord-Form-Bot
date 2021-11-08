import discord
import os
import Botv2
from replit import db
from keep_alive import keep_alive
import asyncio
import pytz
import datetime

token = os.environ['TOKEN']

client = discord.Client()

async def loop():
  while True:
    database = db["database"]
    est = pytz.timezone('US/Eastern')
    if datetime.datetime.today().weekday() < 5:
      now = datetime.datetime.now().astimezone(est)
      current_time = now.strftime("%H")
      if current_time == "07":
        Botv2.execute(database)
        channel = client.get_channel(428729686185476097)
        await channel.send("It's 7 AM!\n" + "Total Run Time: " + str(Botv2.total_run_time) + " Seconds.")
        await asyncio.sleep(3600)
      else:
        await asyncio.sleep(60)
    else:
      await asyncio.sleep(60)


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
  else:
    return 1


@client.event
async def on_ready():
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
    await message.channel.send("Commands\n\n$whoami | check your discord tag\n\n$append Firstname Lastname Email School | add yourself to the list\n\nList of schools:\nsiths\nndhs\n\n$remove index_number | remove yourself from the list\n\n$clear | clear the list *caution*\n\n$show | show the list")

  if msg.startswith("$run"):
    database = db["database"]
    Botv2.execute(database)
    await message.channel.send("Finished!\nTotal Run Time: " + str(Botv2.total_run_time) + " Seconds")

  if msg.startswith("$append"):
    fname = msg.split()[1]
    lname = msg.split()[2]
    email = msg.split()[3]
    school = msg.split()[4]
    update_add(fname, lname, email, school)
    database = db["database"]
    await message.channel.send("Added!\n" + str(db["database"]))

  if msg.startswith("$remove"):
    if "databse" in db.keys():
      index = int(msg.split()[1])
      update_del(index)
      database = db["database"]
      await message.channel.send("Removed!\n" + str(database))

  if msg.startswith("$clear"):
    db.clear()
    database = []
    db["database"] = database
    database = db["database"]
    await message.channel.send("Cleared!\n" + str(database))

  if msg.startswith("$show"):
    database = db["database"]
    await message.channel.send("Here's the list!\n" + str(database))

keep_alive()
client.loop.create_task(loop())
client.run(token)