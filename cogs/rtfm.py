from discord.ext import commands, menus
import discord, random
import utils
from discord.ext.menus.views import ViewMenuPages


class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def rtfm_lookup(self, program=None, *, args=None):

        if not args:
            return self.bot.rtfm_libraries.get(program)

        else:
            url = self.bot.rtfm_libraries.get(program)

            results = await self.bot.scraper.search(args, page=url)

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
            embed.description = "\n".join(f"[`{result}`]({value})" for result, value in results)

            reference = utils.reference(ctx.message)
            await ctx.send(embed=embed, reference=reference)

    @commands.group(
        aliases=["rtd", "rtfs"],
        invoke_without_command=True,
        brief="most of this is based on R.danny including the reference(but this is my own code). But it's my own implentation of it",
    )
    async def rtfm(self, ctx, *, args=None):

        await ctx.trigger_typing()
        results = await self.rtfm_lookup(program="dpy-latest", args=args)
        await self.rtfm_send(ctx, results)

    class RtfmEmbed(menus.ListPageSource):
        async def format_page(self, menu, item):
            embed = discord.Embed(title="Packages:", description=item, color=random.randint(0, 16777215))
            return embed

    @commands.command(brief="a command to view the rtfm DB")
    async def rtfm_view(self, ctx):
        pag = commands.Paginator(prefix="", suffix="")
        for g in self.bot.rtfm_libraries:
            pag.add_line(f"{g} : {self.bot.rtfm_libraries.get(g)}")

        menu = ViewMenuPages(self.RtfmEmbed(pag.pages, per_page=1), delete_message_after=True)
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(DevTools(bot))
