from random import randint
import discord
from discord.ext import commands

from classes.Time import Time

import hdb3

class SellButton(discord.ui.Button):
  def __init__(self, card, cost):
    self.card = card
    self.cost = cost
    super().__init__(
      label="Sell",
      style=discord.ButtonStyle.success,
      emoji="<a:guramoni:914062627402027048>"
    )

  async def callback(self, interaction):
    if card['owner'] != interaction.user.id:
      return await interaction.response.send_message("OI, you don't own this card! <:oiina:914061383602171924>")
    res = await hdb3.inc_bal(interaction.user.id, cost)
    await hdb3.remove_card(card['card_id'])
    await interation.response.send_message(
      embed=discord.Embed(
        title="Balance",
        description=f"Sold Card For: {cost}\n New Balance: {res['bal']}",
        color=self.bot.color
      )
    )
    self.label = "Sold!"
    self.style = discord.ButtonStyle.danger
    self.disabled = True
    await interaction.message.edit(view=self.view)

class Card(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    name="daily"
  )
  @commands.cooldown(1, per=24.0*3600.0)
  async def daily(self, ctx: commands.Context):
    await hdb3.init_user(ctx.author.id)
    amount = randint(500, 1500)
    await hdb3.inc_bal(ctx.author.id, amount)
    user = await hdb3.get_user(ctx.author.id)
    await ctx.send(
      embed=discord.Embed(
        title=f"You Have Dailied and gained: {amount}",
        description=f"New Balance: `{user['bal']}` vyen",
        color=self.bot.color
      )
    )

  @commands.command()
  @commands.cooldown(1, per=15.0)
  async def work(self, ctx: commands.Context):
    await hdb3.init_user(ctx.author.id)
    amount = randint(50, 150)
    await hdb3.inc_bal(ctx.author.id, amount)
    user = await hdb3.get_user(ctx.author.id)
    await ctx.send(
      embed=discord.Embed(
        title=f"You Have Worked and gained: {amount}",
        description=f"New Balance: `{user['bal']}` vyen",
        color=self.bot.color
      )
    )


  @commands.command(
    name="collect"
  )
  async def collect(self, ctx: commands.Context):
    await hdb3.init_user(ctx.author.id)
    vtuber, rarity, card = await hdb3.create_card(ctx.author.id)

    cost = hdb3.get_cost(int(vtuber['subscriber_count']), rarity)

    embed = discord.Embed(
      title=f"Vtuber Found: {vtuber['name']}",
      description=f"Rarity: {rarity[0].lower()}\nOrginazation: {vtuber['org']}\nSub Count: {vtuber['subscriber_count']}\nCard ID: {card['card_id']}\nCost: {cost}",
      color=self.bot.color
    )

    if vtuber['photo'] is not None:
      embed.set_image(url=vtuber['photo'])

    await ctx.send(
      embed=embed,
      view=discord.ui.View(SellButton(card, cost))
    )

  @commands.command(
    name="list"
  )
  async def _list(self, ctx: commands.Context, page: int = 0):
    await hdb3.init_user(ctx.author.id)

    res = await hdb3.get_user_cards(ctx.author.id)

    _min = min(10, len(res))
    cards = [res[i] for i in range(page * _min, page * _min + _min)]

    desc = "Card ID | Vtuber Name\n"
    for i in cards:
      vtuber = await hdb3.get_vtuber(i['vtuber_id'])
      desc += f"[`{i['card_id']} | {vtuber['name']}`](https://www.youtube.com/channel/{i['vtuber_id']}/featured)\n"

    desc += ""

    embed = discord.Embed(
      title="Inventory",
      description=desc,
      color=self.bot.color
    )

    await ctx.send(
      embed=embed
    )

  @commands.command()
  async def view(self, ctx: commands.Context, card_id: int):
    card = await hdb3.get_card(card_id)
    if card['owner'] != ctx.author.id:
      await ctx.send(content="You dont own this card")
      return
    else:
      vtuber = await hdb3.get_vtuber(card['vtuber_id'])
      rarity = hdb3.Rarity.get_value(card['rarity'])

      cost = hdb3.get_cost(int(vtuber['subscriber_count']), rarity)

      embed = discord.Embed(
        title=f"Vtuber Found: {vtuber['name']}",
        description=f"Rarity: {rarity[0].lower()}\nOrginazation: {vtuber['org']}\nSub Count: {vtuber['subscriber_count']}\nCard ID: {card['card_id']}\nCost: {cost}",
        color=self.bot.color
      )

      if vtuber['photo'] is not None:
        embed.set_image(url=vtuber['photo'])

      await ctx.send(
        embed=embed,
        components=[
          Button(
            label="Sell",
            style=ButtonStyle.green,
            custom_id=f"dc {card['card_id']}"
          )
        ]
      )

  @commands.command()
  async def bal(self, ctx):
    user = await hdb3.get_user(ctx.author.id)

    embed = discord.Embed(
      title="Balance",
      description=f"Your Balance is:\n```py\n{user['bal']}\n```",
      color=self.bot.color
    )

    await ctx.send(
      embed=embed
    )

  @commands.command()
  async def sell(self, ctx: commands.Context, card_id: int):
    cost, card, vtuber = await hdb3.get_card_cost(card_id)
    if card['owner'] != ctx.author.id:
      await ctx.send(content="You Dont own this card")
    else:

      await hdb3.remove_card(card_id)
      res = await hdb3.inc_bal(ctx.author.id, cost)
      await ctx.send(
        embed=discord.Embed(
          title=f"Sold: {vtuber['name']}",
          description=f"Sold Card For: `{cost}` vyen\nNew Balance: `{res['bal']}`",
          color=self.bot.color
        )
      )
      del cost, card, vtuber, res




def setup(bot):
  bot.add_cog(Card(bot))
