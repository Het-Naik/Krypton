import discord, os, random
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents, help_command = None, case_insensitive = True, status = discord.Status.idle, activity = discord.Game(name = 'type  `help'))

colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]
afkdict = {}
blacklists = []


@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):
    global colors
    global afkdict
    global blacklists
    if message.author in afkdict:
        afkdict.pop(message.author)
        await message.channel.send(f"Welcome back {message.author}. Removed your afk")

    for member in message.mentions:
        if member != message.author:

            if member in afkdict:
                afkmsg = afkdict[member]

                if afkmsg == "":
                    await message.channel.send(f"{message.author.mention} {member} is afk.")

                else:
                    await message.channel.send(f" {member} is afk - {afkmsg}")

    await client.process_commands(message)

    if message.author.id in blacklists:
        await message.delete()

@commands.command()
async def afk(ctx, *, afkmsg = ""):

    if ctx.message.author in afkdict:
        afkdict.pop(ctx.message.author)
        await ctx.channel.send('you are no longer afk')
    else:
        if afkmsg == "":
            afkdict[ctx.message.author] = afkmsg
            await ctx.channel.send(f"You are now afk.")
        else:
            afkdict[ctx.message.author] = afkmsg
            await ctx.channel.send(f"You are now afk with excuse - {afkmsg}")

@client.command()
async def blacklist(ctx, id: int):
    global blacklists
    if ctx.author.id == 758921556385726494:
        if id in blacklists:
            if id == 802381398399909929 or id == 758921556385726494:
                await ctx.channel.send("no")
            else:
                blacklists.remove(id)
                await ctx.channel.send(f"removed blacklist of {id}")

        else:
            if id == 802381398399909929 or id == 758921556385726494:
                await ctx.channel.send("no")
            else:
                blacklists.append(id)
                await ctx.channel.send(f"blacklisted {id}")

    else:
        await ctx.channel.send("<:nikallavde:817377564170518549>")


class MyHelp(commands.HelpCommand):

    async def send_command_help(self, command):
        embed = discord.Embed(title = self.get_command_signature(command), color = random.choice(colors))
        embed.add_field(name = "Description", value = command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name = "Aliases", value = ", ".join(alias), inline = False)

        channel = self.get_destination()
        await channel.send(embed = embed)


client.help_command = MyHelp()

for file in os.listdir('.commands'):
    if file.endswith('.py') and not file.startswith('_'):
        client.load_extension(f'commands.{file[:-3]}')
        print(f'Loaded the category: {file}')

client.run('BotToken')
