import os
import discord
import re
import aiohttp
import os
import traceback
import logging
import doc_search
from discord.ext import commands
import dotenv
import asqlite

dotenv.load_dotenv()


async def get_prefix(client, message):
    extras = ["smg4*", "smg*", "s*"]
    comp = re.compile("^(" + "|".join(map(re.escape, extras)) + ").*", flags=re.I)
    match = comp.match(message.content)

    if match is not None:
        extras.append(match.group(1))
    return commands.when_mentioned_or(*extras)(client, message)


async def startup(self):
    await self.wait_until_ready()
    await self.tree.sync()
    print("Sucessfully synced applications commands")
    print(f"Connected as {self.user}")


class SMG4Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()
        self.db = await asqlite.connect("bot.db")
        cur = await self.db.cursor()
        cursor = await cur.execute("SELECT * FROM RTFM_DICTIONARY")
        self.rtfm_libraries = dict(await cursor.fetchall())
        self.scraper = doc_search.AsyncScraper(session=self.session)
        await super().start(*args, **kwargs)

    async def close(self):
        await self.session.close()
        await self.db.close()
        await super().close()

    async def setup_hook(self):
        self.loop.create_task(startup(self))

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                except commands.errors.ExtensionError:
                    traceback.print_exc()


bot = SMG4Bot(command_prefix=(get_prefix), intents=discord.Intents.all())


@bot.event
async def on_error(event, *args, **kwargs):
    more_information = os.sys.exc_info()
    error_wanted = traceback.format_exc()
    traceback.print_exc()
    # print(more_information[0])


logging.basicConfig(level=logging.INFO)

bot.run(os.environ["TOKEN"])
