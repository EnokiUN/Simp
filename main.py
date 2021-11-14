import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()


token = os.getenv("TOKEN")

bot = commands.Bot(
  command_prefix=".",
  owner_ids={ 635959963134459904 }
)
bot.friends_ids = { 395899902867275787 }
bot.color = discord.Color.from_rgb(100, 170, 230)

@bot.event
async def on_ready():
  print(f"{bot.user} has logged in!")

cogs = [f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")]

for cog in cogs:
  try:
    bot.load_extension(cog)
  except Exception as err:
    print(err)

bot.run(token)
