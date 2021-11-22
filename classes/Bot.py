from discord.ext import commands
import discord
from discord_components import DiscordComponents

COLOR = discord.Color.from_rgb(100, 180, 180)


class Bot(commands.Bot):
  def __init__(self, command_prefix, help_command=commands.help.DefaultHelpCommand(), description=None, **options):
    super().__init__(command_prefix, help_command=help_command, description=description, **options)
    DiscordComponents(self)

    self.friends_ids = { 395899902867275787 }
    self.color = COLOR

    class MyHelpCommand(commands.MinimalHelpCommand):
      async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=COLOR, description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

    self.help_command = MyHelpCommand()
