import discord
from discord.ext import commands

from hdb import Card, VtuberEntry, Data as HData

class Data(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group()
  async def data(self, ctx):
    pass

  @data.command()
  async def find(self, ctx: commands.Context, *, query: str):
    res = HData.DEX.autocomplete_result(query=query)
    data = res.json()

    desc = ""
    for i in data:
      desc += f"[`{i['text']} : {i['value']}`](https://www.youtube.com/channel/{i['value']}/featured)\n"

    embed = discord.Embed(
      title="Search Results",
      description=desc,
      color=self.bot.color
    )

    await ctx.send(
      embed=embed
    )


  @data.command(
    name="vtuber"
  )
  async def vtuber(self, ctx: commands.Context, vtuber_id: str):
    vtuber = VtuberEntry.get(vtuber_id)
    desc = ""
    for key in VtuberEntry.keys:
      if key in ["photo", "top_topics", "type"]:
        continue
      desc += f"{key.replace('_', ' ')}: {getattr(vtuber, key)}\n"

    embed = discord.Embed(
      title=f"Vtuber: {vtuber.name}",
      description=desc,
      color=self.bot.color
    )

    if vtuber.photo is not None:
      embed.set_image(url=vtuber.photo)

    await ctx.send(
      embed=embed
    )

def setup(bot):
  bot.add_cog(Data(bot))
