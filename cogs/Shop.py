import discord
from discord.ext import commands
from discord_components import Button, Select, SelectOption, ActionRow, ButtonStyle, Interaction

class Shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group()
  async def shop(self, ctx: commands.Context):
    pass

  @shop.command()
  async def page(self, ctx: commands.Context, page: int):
    pass

def setup(bot):
  bot.add_cog(Shop(bot))
