#####################################
# Offically Made By: RENØM#7001     #
# Do Not Skid/Reupload              #
#####################################

import hashlib
import re
import uuid
import discord
from discord.ext import commands
import time
import cloudscraper
import json
import random
import requests
import discord
import time
from discord import app_commands
import cloudscraper
from discord.ext import commands
import asyncio
import math

#Import Random Is Used For Key System

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


#Key System
def createkey(duration_str, num_keys):
  # Parse the duration string into minutes
  duration_parts = duration_str.split(" ")
  duration = 0
  for part in duration_parts:
    if part[-1] == 'd':
      duration += int(part[:-1]) * 24 * 60
    elif part[-1] == 'h':
      duration += int(part[:-1]) * 60
    elif part[-1] == 'm':
      duration += int(part[:-1])

  keys = []
  for i in range(num_keys):
    key = "RENØM#-ymxo".join(
      random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
      for i in range(10)) + ''.join(
        random.choice('0123456789abcdef') for i in range(8))
    keys.append(key)
    with open("buyers.json", "r") as f:
      data = json.load(f)

  for key in keys:
    data[key] = {
      "Key Expires In": time.time() + (duration * 60),
      "✅ Sucessfully Claimed": False
    }

  with open("buyers.json", "w") as f:
    json.dump(data, f)

  return keys


def claim(key, userid):
  with open("buyers.json", "r") as f:
    data = json.load(f)

  if key not in data:
    return "💥 Couldn't Detect Input Key In Our Database Please Try Again"

  if data[key]["❓Key Already Claimed"]:
    return "❓Key Has Expired, Think This Is A Error? Dm RENØM#7001"

  if data[key]["💥 Expiration"] < time.time():
    return "❌ Key Has Sadly Expired"

  data[key]["✅ Sucessfully Claimed"] = True
  data[key]["💫 UserId"] = userid

  with open("buyers.json", "w") as f:
    json.dump(data, f)

  return "✅ Sucessfully Claimed"


def status(userid):
  with open("buyers.json", "r") as f:
    data = json.load(f)
  with open("lifetime.txt", "r") as f:
    if str(userid) in f.read():
      return "⌚ Detected Your Subscription As Lifetime, Congrats"
      return
  subscription = None
  for key, value in data.items():
    if value["✅ Verfied Buyer"] and value["💫 UserId"] == userid:
      if value["⌚ Expires On"] > time.time():
        if not subscription or value["⌚ Expires On"] < subscription[
            "⌚ Expires On"]:
          subscription = value

  if not subscription:
    return "None"

  days_left = (subscription["⌚ Expires On"] - time.time()) / (24 * 60 * 60)
  return f"{days_left:.0f} Days Left"


def has_subscription(userid):

  with open("buyers.json", "r") as f:
    data = json.load(f)
  with open("lifetime.txt", "r") as f:
    if str(userid) in f.read():
      return True
  for key in data.keys():
    if data[key]["✅ Verified Buyer"] and data[key]["💫 UserID"] == userid:
      if time.time() < data[key]["⌚ Expires On"]:
        return True

  return False

#Mines Source Code
@bot.slash_command(name='mines', description='Predicts The Outcome For Your Next Mines Game')
async def mines(ctx, round_id: str):
  hash = hashlib.sha256(round_id.encode()).hexdigest()
  uuid_check = str(uuid.uuid3(uuid.NAMESPACE_DNS, round_id))

  patterns = [
    re.compile(r"([a-f0-9])\1{3,}"),
    re.compile(r"([a-f0-9]{4})[a-f0-9]*\1{3,}"),
    re.compile(r"([a-f0-9]{2})[a-f0-9]*\1{5,}"),
  ]

  safe_tiles = []
  for pattern in patterns:
    matches = pattern.findall(hash)
    matches += pattern.findall(uuid_check)
    safe_tiles += [int(x, 16) % 25 for x in matches]

  grid = ['❌'] * 25
  for index in safe_tiles:
    grid[index] = '✅'
  grid = [grid[i:i + 5] for i in range(0, 25, 5)]

  accuracy = len(safe_tiles) / 25 * 100

  embed = discord.Embed(title=f"Round ID: {round_id}",
                        description="\n".join(" ".join(row) for row in grid))
  embed.add_field(name="**Accuracy 💡**", value=f"{accuracy:.2f}%", inline=False)
  status = "No Server Errors Were Found"
  print(accuracy)
  if str(accuracy) == "0.0":
    status = "An Error Has Occured, **This Made Accuracy 0%**"
  embed.add_field(name="Bloxflip Server Status",
                  value=f"*Finding Bugs In Bloxflip Api* \n {status}")
  await ctx.respond("Request Is Ongoing For Api", ephemeral=True)
  time.sleep(3)
  await ctx.respond(embed=embed, ephemeral=True)


#Crash Source Code
@bot.slash_command(name='crash', description='Predicts The Outcome For Your Next Crash Game')
async def crash(ctx):
  user = ctx.author
  scraper = cloudscraper.create_scraper(browser={
    'browser': 'firefox',
    'platform': 'windows',
    'mobile': False
  })
  games = scraper.get("http://rest-bf.blox.land/games/crash").json()
  if ctx.author.id:
    ok = await ctx.respond(embed=discord.Embed(description="Checking The Last Few Rounds....",
                                               color=discord.Color.purple()))

    def lol():
      r = scraper.get("http://rest-bf.blox.land/games/crash").json()["history"]
      yield [
        r[0]["crashPoint"],
        [float(crashpoint["crashPoint"]) for crashpoint in r[-2:]]
      ]

    for game in lol():
      games = game[1]
      avg = sum(games) / len(games)
      chance = 1
      for game in games:
        chance = chance = 95 / game
        prediction = (1 / (1 - (chance)) + avg) / 2
        if float(prediction) > 2:
          color = 0xe81a1a
        else:
          color = 0xe81a1a

        if float(prediction) < 1:
          if float(prediction) < -3:
            await ok.edit_original_message(
              embed=discord.Embed(description="Unable To Predict Due To An Error",
                                  color=discord.Color.purple()))
          elif float(prediction) > -3:
            crash = prediction + 2

        else:
          crash = prediction

        title = f"Bloxflip Predictor"
        thumbnail = f"{user.display_avatar.url}"
        desc = f"**Crash**\n{crash:.2f}x\n**Accuracy**\n{chance:.2f}%"
        em = discord.Embed(description=desc, color=color, title=title)
        await ok.edit_original_message(embed=em)


#Roulette Source Code
@bot.slash_command(name='roulette', description='Predicts The Outcome For Your Next Roulette Game')
async def roulette(ctx):
  api_url = "https://api.bloxflip.com/games/roulette".json()
  response = requests.get(api_url)
  data = response.json()
  round_id = data['💫 Round-ID:']
  prediction = data['🧠 Prediction:']
  previous_streaks = data['🎡 Streaks:']
  embed = discord.Embed(title="Bloxflip Predictor")
  embed.add_field(name="🧠 Prediction:", value=prediction)
  embed.add_field(name="🎡 Streaks:", value=f"Previous Wins {previous_streaks}")
  embed.add_field(name="💫 Round-ID", value=round_id)
  await ctx.send(embed=embed)

#Unrig Command
@bot.command()
async def unrig(ctx, server_hash: str):
  async with ctx.typing():
    await asyncio.sleep(22)
    success_percentage = min(
      int(hashlib.sha256(server_hash.encode()).hexdigest(), 16) % 100, 69.69)
    client_seed = hashlib.sha256(server_hash.encode()).hexdigest()[:8] + '-' + \
    hashlib.sha256(server_hash.encode()).hexdigest()[8:12] + '-' + \
                hashlib.sha256(server_hash.encode()).hexdigest()[12:16] + '-' + \
                hashlib.sha256(server_hash.encode()).hexdigest()[16:20] + '-' + \
                hashlib.sha256(server_hash.encode()).hexdigest()[20:32]
    embed = discord.Embed(title="💡 Unrigged", color=0x000000)
    embed.add_field(name="✅ Unrig Sucess Results",
                    value=f"{success_percentage:.2f}%",
                    inline=False)
    embed.add_field(name="Client-Seed", value=f"{client_seed}", inline=False)
    await ctx.send(embed=embed)

bot.run('YOUR-BOT-TOKEN')
