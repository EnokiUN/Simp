import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import logging
# from app import keep_alive
import asyncio
import random

from classes.Bot import Bot


logging.basicConfig(
  filename="logs.log",
  filemode="a",
  format="[%(asctime)s::%(name)s::%(module)s]:\n\t(args: %(args)s)\n%(levelname)s - %(message)s",
  level="DEBUG"
)

load_dotenv()


# keep_alive(with_join=False)


token = os.getenv("TOKEN")

prefix = commands.when_mentioned_or(".")

bot = Bot(
  command_prefix=".",
  owner_ids={ 635959963134459904 }
)

@bot.event
async def on_ready():
  print(f"{bot.user} has logged in!")

def run():
  cogs = [f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")]

  for cog in cogs:
    try:
      print(f'registering cog: {cog}')
      bot.load_extension(cog)
    except Exception as err:
      print(err)

  bot.run(token)


if __name__ == "__main__":
  run()
