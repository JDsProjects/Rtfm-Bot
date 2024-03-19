from __future__ import annotations

import logging
import traceback
from os import getenv as os_getenv
from re import IGNORECASE
from re import compile as re_compile
from re import escape as re_escape
from typing import TYPE_CHECKING, Any, List, Match, Optional, Pattern, TypedDict

from aiohttp import ClientSession
from asqlite import connect as asqlite_connect
from discord import Intents
from discord.ext import commands

if TYPE_CHECKING:
    from sqlite3 import Row

    from asqlite import Connection, Cursor
    from discord import Message
    from discord.ext.commands.bot import PrefixType
    from typing_extensions import Self

    class RTFMLibraryData(TypedDict):
        name: str
        link: str

from cogs import EXTENSIONS

async def get_prefix(client: RTFMBot, message: Message) -> list[str]:
    extras: list[str] = ["rtfm*", "rm*", "r*"]
    comp: Pattern[str] = re_compile("^(" + "|".join(map(re_escape, extras)) + ").*", flags=IGNORECASE)
    match: Optional[Match[str]] = comp.match(message.content)

    if match is not None:
        extras.append(match.group(1))

    return commands.when_mentioned_or(*extras)(client, message)


class RTFMBot(commands.Bot):
    def __init__(self, *, command_prefix: PrefixType[Self], intents: Intents) -> None:
        super().__init__(command_prefix=command_prefix, intents=intents)

        # filled in by setup_hook
        self.db: Optional[Connection] = None
        self.session: Optional[ClientSession] = None
        self.rtfm_libraries: dict[str, str] = {}

    async def setup_hook(self) -> None:
        # load extensions
        
        for cog in EXTENSIONS:
            try:
                await self.load_extension(f"{cog}")
            except commands.errors.ExtensionError:
                traceback.print_exc()

        # initialize global aiohttp session
        self.session = ClientSession()

        # load rtfm libraries
        self.db = await asqlite_connect("bot.db")
        main_cursor: Cursor = await self.db.cursor()
        result: Cursor = await main_cursor.execute("SELECT * FROM RTFM_DICTIONARY ORDER BY NAME ASC")

        rtfm_libraries: list[Row[str]] = await result.fetchall()
        self.rtfm_libraries = dict(rtfm_libraries)  # type: ignore # this is supported.

        

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
        if self.db:
            await self.db.close()
        await super().close()


bot = RTFMBot(command_prefix=get_prefix, intents=Intents(messages=True, message_content=True, guilds=True))


@bot.event
async def on_error(event: str, *args: Any, **kwargs: Any) -> None:
    # from sys import exc_info as sys_exc_info
    # more_information = sys_exc_info()
    # error_wanted = traceback.format_exc()
    # default behaviour:
    traceback.print_exc()
    # print(more_information[0])


logging.basicConfig(level=logging.INFO)

bot.run(os_getenv("TOKEN"))
