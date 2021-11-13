import B
import discord, re, aiohttp
from discord.ext import commands

async def get_prefix(client, message):
  extras = ["smg4*", "smg*", "s*"]
  comp = re.compile("^(" + "|".join(map(re.escape, extras)) + ").*", flags = re.I)
  match = comp.match(message.content)

  if match is not None:
    extras.append(match.group(1))
  return commands.when_mentioned_or(*extras)(client, message)


class SMG4Bot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def start(self, *args, **kwargs):
    self.session = aiohttp.ClientSession()
    await super().start(*args, **kwargs)

  async def close(self):
    await self.session.close()
    await super().close() 

bot = SMG4Bot(command_prefix = (get_prefix),intents = discord.Intents.all())

bot.load_extension('jishaku')

B.b()