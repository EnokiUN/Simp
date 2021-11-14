import discord
from discord.ext import commands

from database import get_randoms
from db import Card, add_card, find_vtuber, get_user, sell_card
from src.holodex import Entry

from util import CommandWithCooldown, owner_ids

class _Card(commands.Cog, name="Card"):
  def __init__(self, bot):
    self.bot: commands.Bot = bot

  @commands.group()
  async def card(self, ctx):
    pass

  @card.command(
    name="generate",
    hidden=True
  )
  async def generate(self, ctx: commands.Context, target: discord.User, vtuber_id: str, rarity: int):
    if ctx.author.id not in owner_ids:
      await ctx.send("You Don't Have permission to use this command")
      return
    else:
      targ = await get_user(target.id)
      new_card = Card(
        vtuber_id=vtuber_id,
        rarity=rarity,
        xp=0
      )
      await add_card(target.id, new_card)

      vtuber = Card.get_vtuber(vtuber_id=vtuber_id)

      embed = discord.Embed(
        title=f"Vtuber Found: **{vtuber.name}**",
        description=self.generate_description(new_card, vtuber),
        color=self.bot.color
      )

      if vtuber.photo is not None:
        embed.set_image(url=vtuber.photo)

      await ctx.send(
        embed=embed
      )




  def generate_description(self, card: Card, vtuber: Entry):
    return "".join([
      f"Name: {vtuber.name}\n",
      f"Organization: {vtuber.org}\n",
      f"Video Count: {vtuber.video_count}\n",
      f"Clip Count: {vtuber.clip_count}\n",
      f"Rarity: {card.rarity[0].lower()}"
    ])

  @card.command(
    name="collect", cls=CommandWithCooldown
  )
  @commands.cooldown(1, 60.0)
  async def collect(self, ctx: commands.Context):
    user = await get_user(ctx.author.id)
    vtuber = get_randoms(1)[0]

    new_card = Card.generate(vtuber.id)

    await add_card(ctx.author.id, new_card)

    embed = discord.Embed(
      title=f"Vtuber Found: **{vtuber.name}**",
      description=self.generate_description(new_card, vtuber),
      color=self.bot.color
    )

    if vtuber.photo is not None:
      embed.set_image(url=vtuber.photo)

    await ctx.send(
      embed=embed
    )

  async def get_page(self, cards: list, page: int = 0) -> list:
    out = []
    _max = min(10, len(cards))
    _cur = page * 10
    for i in range(_cur, min(_cur + _max, len(cards))):
      out.append((i, cards[i]))
    return out

  @card.command(name="list")
  async def _list(self, ctx: commands.Context, page: int = 0):
    user = await get_user(ctx.author.id)
    cards = await self.get_page(user['cards'], page)

    desc = ""
    for idx, _card in cards:
      card = Card.from_data(_card)
      vtuber = Card.get_vtuber(card.vtuber_id)
      desc += f"`{idx}`|[{card.rarity[0].lower()}] {vtuber.name} (org: {vtuber.org})\n"

    await ctx.send(
      embed= discord.Embed(
        title="Card List",
        description=desc,
        color=self.bot.color
      )
    )

  @card.command()
  async def _find(self, ctx: commands.Context, _min=0.8, *, query: str):
    out = find_vtuber(query, _min=_min)
    desc = ''
    for i in range(min(len(out), 10)):
      desc += f"`{i}`| {out[i].name} : {out[i].vtuber_id}"

    await ctx.send(
      embed=discord.Embed(
        title="results",
        description=desc,
        color=self.bot.color
      )
    )

  @card.command()
  async def sell(self, ctx: commands.Context, card_id: int):
    user = await get_user(ctx.author.id)
    cards = user['cards']

    if card_id > len(cards):
      await ctx.send("Card Index out of range")
      return


    res = await sell_card(ctx.author.id, cards[card_id])
    await ctx.send("done")



def setup(bot):
  bot.add_cog(_Card(bot))
