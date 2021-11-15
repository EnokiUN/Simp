import discord
from discord.ext import commands
import os
import logging
import sys
import traceback


class Dev(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot

  @property
  def cog_files(self) -> list[str]:
    return [f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")]


  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
      """A global error handler cog."""


      trace = "".join(traceback.format_exception(type(error), error, error.__traceback__))

      logging.error(trace)


      if isinstance(error, commands.CommandNotFound):
          return  # Return because we don't want to show an error for every command not found
      elif isinstance(error, commands.CommandOnCooldown):
          message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
      elif isinstance(error, commands.MissingPermissions):
          message = "You are missing the required permissions to run this command!"
      elif isinstance(error, commands.UserInputError):
          message = "Something about your input was wrong, please check your input and try again!"
      elif isinstance(error, commands.DisabledCommand):
          message = f'{ctx.command} has been disabled.'
      else:
          message = f"```\n{trace}\n```"

      await ctx.send(embed=discord.Embed(
        title=f"**{error.__class__.__name__}**",
        description=message,
        color=self.bot.color
      ))


  @commands.group()
  async def cog(self, ctx: commands.Context):
    pass

  @cog.command()
  async def files(self, ctx: commands.Context):
    await ctx.send(
      embed=discord.Embed(
        title="Cog Files",
        description="".join([f"{idx}: `{name}`\n" for idx, name in enumerate(self.cog_files)])
      )
    )

  async def say_done(self, ctx: commands.Context):
    await ctx.send(content="done", delete_after=5.0)

  @cog.command()
  async def load(self, ctx: commands.Context, *, extension: str):
    self.bot.load_extension(extension)
    await self.say_done(ctx)

  @cog.command()
  async def reload(self, ctx: commands.Context, *, extension: str):
    self.bot.reload_extension(extension)
    await self.say_done(ctx)

  @cog.command()
  async def unload(self, ctx: commands.Context, *, extension: str):
    self.bot.reload_extension(extension)
    await self.say_done(ctx)





def setup(bot):
  bot.add_cog(Dev(bot))
