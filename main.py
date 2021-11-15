import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
  filename="logs.log",
  filemode="a",
  format="[%(asctime)s::%(name)s::%(module)s]:\n\t(args: %(args)s)\n%(levelname)s - %(message)s",
  level="DEBUG"
)

load_dotenv()


token = os.getenv("TOKEN")

prefix = commands.when_mentioned_or(".")


class Bot(commands.Bot):
  def __init__(self, command_prefix, help_command=commands.help.DefaultHelpCommand(), description=None, **options):
    super().__init__(command_prefix, help_command=help_command, description=description, **options)

    self.friends_ids = { 395899902867275787 }
    self.color = discord.Color.from_rgb(100, 170, 230)




bot = Bot(
  command_prefix=".",
  owner_ids={ 635959963134459904 }
)

@bot.event
async def on_ready():
  print(f"{bot.user} has logged in!")

cogs = [f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")]

for cog in cogs:
  try:
    print(f'registering cog: {cog}')
    bot.load_extension(cog)
  except Exception as err:
    print(err)

bot.run(token)
