import discord
from discord.ext import commands


class General(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot

  @commands.command(
    name="ping",
    aliases=["latency"]
  )
  async def ping(self, ctx: commands.Context):
    await ctx.send(
      embed=discord.Embed(
        title="Latency",
        description=f"My Ping is: {round(self.bot.latency * 100, 2)}ms"
      )
    )


def setup(bot):
  bot.add_cog(General(bot))
