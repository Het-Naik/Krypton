import discord, random, datetime
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests as r
intents = discord.Intents.all()
colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]


class Images(commands.Cog, name='Images'):
    @commands.command()
    async def harvard(self, ctx, *, txt: str):
        img = Image.open("/Users/mukti/Kr6pton/Assets/hwtkyl.jpg")
        draw = ImageDraw.Draw(img)
        size = 40
        if len(txt) < 10:
            size = 40
            work = True
        elif len(txt) < 20:
            size = 35
            work = True
        elif 20 <= len(txt) < 30:
            size = 30
            work = True
        elif 30 <= len(txt) < 40:
            size = 25
            work = True
        elif 40 <= len(txt) <= 50:
            size = 20
            work = True
        else:
            work = False
        if work:
            font = ImageFont.truetype("ARIAL.TTF", size)
            draw.text((20, 120), txt, (0, 0, 0), font = font)
            img.save("
                     /Assets/hwtkyl.jpg")
            await ctx.channel.purge(limit = 1)
            await ctx.channel.send("Processing image. It may take upto 3 seconds.", delete_after = 3)
            await ctx.channel.send(file = discord.File("./Assets/hwtkyl.jpg"))
        else:
            await ctx.channel.send("The text can only be upto 50 characters")

    @commands.command()
    async def notstonks(self, ctx, usr: discord.Member = "author"):
        if usr == "author":
            usr = ctx.author
        await ctx.channel.send("Processing Image. This may take upto 3 seconds", delete_after=3)
        base = Image.open("./Assets/notstonks.jpg")
        face = usr.avatar_url_as(size = 128)
        data1 = BytesIO(await face.read())
        pfp1 = Image.open(data1)
        pfp1 = pfp1.resize((155, 155))
        base.paste(pfp1, (165, 6))
        base.save("./Assets/notstonksedited.jpg")
        await ctx.channel.send(file = discord.File("./Assets/notstonksedited.jpg"))


    @commands.command()
    async def stonks(self, ctx, usr: discord.Member = "author"):
        if usr == "author":
            usr = ctx.author
        await ctx.channel.send("Processing Image. This may take upto 3 seconds", delete_after=3)
        base = Image.open("./Assets/stonks.jpg")
        face = usr.avatar_url_as(size = 128)
        data1 = BytesIO(await face.read())
        pfp1 = Image.open(data1)
        pfp1 = pfp1.resize((340, 340))
        base.paste(pfp1, (150, 75))
        base.save("./Assets/stonks.jpg")
        await ctx.send(file = discord.File("./Assets/stonks.jpg"))


    @commands.command()
    async def meme(self, ctx):
        m = r.get("https://some-random-api.ml/meme")
        a = m.json()["image"]
        c = m.json()["caption"]
        memeem = discord.Embed(title = c, description = "")
        memeem.set_image(url = a)
        await ctx.channel.send(embed = memeem)


    @commands.command()
    async def gay(self, ctx, usr: discord.Member):
        pfp = usr.avatar_url
        url = f"https://some-random-api.ml/canvas/gay?avatar={pfp}"
        url = url.replace("webp?size=1024", "jpg")
        await ctx.channel.send(url)


    @commands.command()
    async def rip(self, ctx, usr: discord.Member):
        pfp = usr.avatar_url
        url = f"https://some-random-api.ml/canvas/wasted?avatar={pfp}"
        url = url.replace("webp?size=1024", "jpg")
        await ctx.channel.send(url)


    @commands.command()
    async def cat(self, ctx):
        q = r.get("https://some-random-api.ml/img/cat")
        lik = q.json()["link"]
        lk = discord.Embed(title = "MEOW :cat2:", description = "", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
        lk.set_image(url = lik)
        await ctx.channel.send(embed = lk)


    @commands.command()
    async def wink(self, ctx):
        q = r.get("https://some-random-api.ml/animu/wink")
        lik = q.json()["link"]
        lk = discord.Embed(title = "WINKKKKKKK :wink:", description = "", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
        lk.set_image(url = lik)
        await ctx.channel.send(embed = lk)


    @commands.command()
    async def dog(self, ctx):
        q = r.get("https://some-random-api.ml/img/dog")
        lik = q.json()["link"]
        lk = discord.Embed(title = "WOOF :dog:", description = "", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
        lk.set_image(url = lik)
        await ctx.channel.send(embed = lk)


    """
    Error Handlers
    """

    @harvard.error
    async def harvard_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            errorEmbed = discord.Embed(title = "Command harvard => Fail", description = "Incorrect arguments passed")
            await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `bet` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    @notstonks.error
    async def notstonks_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            errorEmbed = discord.Embed(title = "Command harvard => Fail", description = "No such member found")
            await ctx.send(embed=errorEmbed)

        else:
            errorEmbed = discord.Embed(title = "Command harvard => Fail", description = "Incorrect arguments passed")
            await ctx.send(embed = errorEmbed)

def setup(client: commands.Bot):
    client.add_cog(Images(client))
