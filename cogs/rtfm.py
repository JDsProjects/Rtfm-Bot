from typing import TYPE_CHECKING, Any, Optional, Union
from random import randint

from discord import AllowedMentions, Embed
from discord.ext import commands

from utils.extra import RTFMEmbedPaginator, reference

if TYPE_CHECKING:
    from main import RTFMBot

    from discord.ext.commands import Context
else:
    Context = Any
    RTFMBot = commands.Bot


class DevTools(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    async def rtfm_lookup(self, program: str, *, library: Optional[str] = None) -> Union[dict[str, str], str]:
        assert self.bot.scraper is not None

        ERROR_MESSAGE = f"Could not find anything with {library}."

        url = self.bot.rtfm_libraries.get(program)
        if not url:
            return ERROR_MESSAGE

        if not library:
            return url

        results = await self.bot.scraper.search(library, page=url)
        if not results:
            return library

        return {name: link for name, link in results}

    async def rtfm_send(self, ctx: Context, results: Union[dict[str, str], str]) -> None:
        if isinstance(results, str):
            await ctx.send(results, allowed_mentions=AllowedMentions.none())
        else:
            embed = Embed(color=randint(0, 16777215))
            embed.description = "\n".join(f"[`{result}`]({value})" for result, value in tuple(results.items())[:10])

            message_reference = reference(ctx.message)
            await ctx.send(embed=embed, reference=message_reference)

    @commands.command(aliases=["rtd", "rtfs"])
    async def rtfm(self, ctx: Context, *, args: Optional[str] = None) -> None:
        """most of this is based on R.danny including the reference(but this is my own code). But it's my own implentation of it"""
        await ctx.typing()
        results = await self.rtfm_lookup(program="dpy-latest", library=args)
        await self.rtfm_send(ctx, results)

    @commands.command()
    async def rtfm_view(self, ctx: Context) -> None:
        """a command to view the rtfm DB"""
        pag = commands.Paginator(prefix="", suffix="")
        for g in self.bot.rtfm_libraries:
            pag.add_line(f"{g} : {self.bot.rtfm_libraries.get(g)}")

        menu = RTFMEmbedPaginator(pag.pages, delete_message_after=True)  # type: ignore
        await menu.start(ctx)


async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(DevTools(bot))
