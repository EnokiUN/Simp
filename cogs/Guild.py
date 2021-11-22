import discord
from discord.ext import commands
import re
import requests
import urllib.request

emoji_regex = re.compile("<((a?):?(.{0,22}):(\d{18}>))")

from classes.Bot import Bot

class Guild(commands.Cog):
  def __init__(self, bot):
    self.bot: Bot = bot

  @commands.command()
  async def add_emote(self, ctx: commands.Context, emoji: str):
    pass



def setup(bot):
  bot.add_cog(Guild(bot))


