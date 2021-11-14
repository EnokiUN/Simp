from discord.ext import commands

owner_ids = { 635959963134459904 }

class CommandWithCooldown(commands.Command):
  async def prepare(self, ctx):
    try:
      return await super().prepare(ctx)
    except commands.CommandOnCooldown as e:
      if ctx.message.author.id in owner_ids:
        return
      else:
        raise e
