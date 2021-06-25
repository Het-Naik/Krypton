import discord, random, datetime, requests, urllib
from discord.ext import commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents, help_command = None, case_insensitive = True, status = discord.Status.idle, activity = discord.Game(name = 'type  `help'))

intents = discord.Intents.all()
colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]

class Utilities(commands.Cog, name='Utilities'):
    @commands.command()
    async def math(self, ctx, *, arg):
        ans = eval(arg)
        await ctx.channel.send(ans)

    @commands.command()
    async def poll(self, ctx, *, qno: str):

        if ':' in qno:
            reactdict = {1: "<:number_1:823055011269050399>", 2: "<:number_2:823055154077106207>", 3: "<:number_3:823055214641807381>", 4: "<:number_4:823055273010659338>", 5: "<:number_5:823055339112103987>", 6: "<:number_6:823055519715295243>", 7: "<:number_7:823055470389887026>", 8: "<:number_8:823055794084904960>", 9: "<:number_9:823055844065017876>"}
            qno = qno.split(':')
            ques = qno[0]
            opts = qno[1]
            pollem = discord.Embed(title = f"{ctx.author}'s poll", description = f"you asked {ques} and the options are : ")

            if ';' in qno[1]:
                opts = opts.split(';')

                for i in range(0, len(opts)):
                    pollem.add_field(name = f"option {i + 1}: {opts [i]}", value = f"react with :{reactdict[i+1]}: if you vote for option {i+1}", inline=False)
                pollreact = await ctx.channel.send(embed=pollem)

                for j in range(len(opts)):
                    await pollreact.add_reaction(reactdict[j+1])

            else:
                await ctx.channel.send("The syntax is `;poll` `ques:opt1;opt2;opt3....opt9`.")

        else:
            await ctx.channel.send("The syntax is `;poll` `ques:opt1;opt2;opt3....opt9`.")


    @commands.command(aliases = ["embed"])
    async def say(self, ctx, *, txt):
        txt = str(txt)
        await ctx.message.delete()
        if ";" in txt:
            text = txt.split(";")
            sayEmbed = discord.Embed(title = f"{text[0]}", description = "f{text[1]}")
            ctx.channel.send(embed=sayEmbed)
        else:
            sayEmbed = discord.Embed(description = txt)
            ctx.channel.send(embed=sayEmbed)

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        await ctx.message.delete()
        suggestionEmbed = discord.Embed(title = f"suggestion by {ctx.author}", description = suggestion, colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
        s = await ctx.channel.send(embed = suggestionEmbed)
        await s.add_reaction("<a:check_ravena:806764521909649438>")
        await s.add_reaction("<a:uncheck_ravena:806764368607838228>")

    @commands.command()
    async def weather(self, ctx, city: str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c4ad4162ff8f2c9371a1492c62bf82b"
        a = requests.get(url)
        longitude = a.json()["coord"]["lon"]
        latitude = a.json()["coord"]["lat"]
        actualTemp = a.json()["main"]["temp"]
        feelTemp = a.json()["main"]["feels_like"]
        await ctx.channel.send(f"temperature : {int(actualTemp - 273.15)}°C\n"
                               f"feels like : {int(feelTemp - 273.15)}°C\n"
                               f"longitude of {city} : {longitude} and latitude of {city} : {latitude}\n")

    @commands.command()
    async def ping(self, ctx):
        pingEmbed = discord.Embed(title = "Ping Status", description = f"The ping of the bot is {(client.latency * 1000)}ms")
        await ctx.channel.send(embed=pingEmbed)

    @commands.command()
    async def shortenurl(self, ctx, urlts, suffix):
        key = 'fcbfd96544b2e5d7b0be060cdb1022c927168'
        urllib.parse.quote(urlts)
        status = requests.get(f'http://cutt.ly/api/api.php?key={key}&short={urlts}&name={suffix}')

        if status.json()["url"]["status"] == 1:
            await ctx.channel.send("Link is already shortened.")
        elif status.json()["url"]["status"] == 2:
            await ctx.channel.send("Enter a valid link.")
        elif status.json()["url"]["status"] == 3:
            await ctx.channel.send("Suffix already taken, please change it.")
        elif status.json()["url"]["status"] == 4:
            await ctx.channel.send("There was a problem connecting to the api.\nContact developer for more info.")
        elif status.json()["url"]["status"] == 5:
            await ctx.channel.send("Link has invalid characters.")
        elif status.json()["url"]["status"] == 6:
            await ctx.channel.send("Can't shorten urls from that domain.")
        elif status.json()["url"]["status"] == 7:
            await ctx.channel.send(f"url successfully shortned.\nNew url : https://cutt.ly/{suffix}")

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            errorEmbed = discord.Embed(title = "Command `weather` => Fail", description = "Incorrect city name")
            await ctx.send(embed=errorEmbed)
            return error
        else:
            return error
def setup(client: commands.Bot):
    client.add_cog(Utilities(client))