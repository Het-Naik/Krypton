import discord, asyncio
from discord.ext import commands

intents = discord.Intents.all()
colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]

class Other(commands.Cog, name='Other'):
    @commands.command()
    async def spam(self, ctx, amt: int, txt):
        if ctx.author.id == 758921556385726494:
            for i in range(amt):
                await ctx.channel.send(txt)
                await asyncio.sleep(0.3)
        else:
            await ctx.channel.send("Nou")


def setup(client: commands.Bot):
    client.add_cog(Other(client))