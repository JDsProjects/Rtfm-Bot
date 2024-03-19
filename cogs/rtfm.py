from random import randint
from typing import TYPE_CHECKING, Any, Optional, Union

from discord import AllowedMentions, Embed
from discord.ext import commands
import discord

from utils.extra import RTFMEmbedPaginator, reference
import utils
from utils import fuzzy, ObjectWrap

if TYPE_CHECKING:
    from discord.ext.commands import Context

    from main import RTFMBot
else:
    Context = Any
    RTFMBot = commands.Bot


class DevTools(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    async def rtfm_lookup(self, url=None, *, args=None):
        if not args:
            return url

        else:
            unfiltered_results = await utils.rtfm(self.bot, url)

            results = fuzzy.finder(args, unfiltered_results, key=lambda t: t[0])

            if not results:
                return f"Could not find anything with {args}."

            else:
                return results

    async def rtfm_send(self, ctx, results):
        if isinstance(results, str):
            await ctx.send(results, allowed_mentions=discord.AllowedMentions.none())

        else:
            embed = discord.Embed(color=random.randint(0, 16777215))

            results = results[:10]

            embed.description = "\n".join(f"[`{result}`]({result.url})" for result in results)

            message_reference = reference(ctx.message)
            await ctx.send(embed=embed, reference=message_reference)


    @commands.command(
        aliases=["rtd", "rtfs", "rtdm"],
        invoke_without_command=True,
        brief="a rtfm command that allows you to lookup at any library we support looking up(using selects)",
    )
    async def rtfm(self, ctx, *, args=None):
        
        libraries = [utils.ObjectWrap(name, url) for (name, url) in self.bot.rtfm_libraries.items()]

        view = utils.RtfmChoice(ctx, libraries, timeout=15.0)
        view.message = await ctx.send(content="Please Pick a library you want to parse", view=view)

        await view.wait()

        await ctx.typing()

        results = await self.rtfm_lookup(url=view.value, args=args)

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
