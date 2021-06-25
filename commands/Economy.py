import discord, json, random, datetime
from discord.ext import commands

intents = discord.Intents.all()
colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]

async def bal_data():
    with open("/Users/mukti/Kr6pton/Assets/balance.json", "r") as f:
        users = json.load(f)
    return users


async def open_acc(user):
    # users = await bal_data()
    with open("/Users/mukti/Kr6pton/Assets/balance.json", "r") as f:
        users = json.load(f)
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 1000
            users[str(user.id)]["bank"] = 1000
            users[str(user.id)]["tesla stocks"] = 0
            users[str(user.id)]["apple stocks"] = 0
            users[str(user.id)]["microsoft stocks"] = 0
            users[str(user.id)]["nvidia stocks"] = 0
            users[str(user.id)]["amd stocks"] = 0
        with open("/Users/mukti/Kr6pton/Assets/balance.json", "w") as h:
            json.dump(users, h)


class Economy(commands.Cog, name="Economy"):

    # The beg command
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self, ctx):
        user = ctx.message.author
        await open_acc(user)
        acc_details = await bal_data()
        earn = random.randrange(101)
        await ctx.channel.send(f"you got {earn} from someone")
        acc_details[str(user.id)]["wallet"] += earn
        with open("/Users/mukti/Kr6pton/Assets/balance.json", "w") as f:
            json.dump(acc_details, f)

    # The betting command
    @commands.command(aliases = ["gamble", "roll"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def bet(self, ctx, val: int):
        user = ctx.author
        acc_details = await bal_data()
        if val <= acc_details[str(user.id)]["wallet"]:
            if val >= 100:
                dice = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                userRoll = random.choice(dice)
                botRoll = random.choice(dice)
                winPercent = random.randrange(70, 200, 10)
                if botRoll > userRoll:
                    if val < acc_details[str(user.id)]["wallet"]:
                        acc_details[str(user.id)]["wallet"] -= val
                        with open("balance.json", "w") as f:
                            json.dump(acc_details, f)
                    else:
                        acc_details[str(user.id)]["wallet"] = 0
                        with open("balance.json", "w") as f:
                            json.dump(acc_details, f)
                    loss = discord.Embed(title = f"{ctx.message.author}'s losing gambling game.", description = f"you lost {val}\nNew balance = {acc_details[str(user.id)]['wallet']}", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
                    loss.add_field(name = f"{ctx.message.author} rolled:", value = f"{userRoll}")
                    loss.add_field(name = f"Krypton rolled:", value = f"{botRoll}")
                    await ctx.channel.send(embed = loss)

                elif userRoll > botRoll:
                    prize = (val * winPercent * 0.01) // 1
                    acc_details[str(user.id)]["wallet"] += prize
                    win = discord.Embed(title = f"{ctx.message.author}'s winning gambling game", description = f"you won {prize}\nNew balance = {acc_details[str(user.id)]['wallet']}",  colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
                    win.add_field(name = f"{ctx.message.author} rolled:", value = f"{userRoll}")
                    win.add_field(name = f"Krypton rolled:", value = f"{botRoll}")
                    await ctx.channel.send(embed = win)
                    with open("balance.json", "w") as f:
                        json.dump(acc_details, f)

                elif userRoll == botRoll:
                    tie = discord.Embed(name = f"{ctx.message.author}'s gamble", description = f"tied", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
                    tie.add_field(name = "your balance isn't changed", value = f"now your wallet has {acc_details[str(user.id)]['wallet']}")
                    tie.add_field(name = f"{ctx.message.author} rolled:", value = f"{userRoll}")
                    tie.add_field(name = f"Krypton rolled:", value = f"{botRoll}")
                    await ctx.channel.send(embed = tie)
                    with open("balance.json", "w") as f:
                        json.dump(acc_details, f)

            else:
                await ctx.channel.send("Sorry you cant bet more less than 100")

        elif val > acc_details[str(user.id)]["wallet"]:
            await ctx.channel.send("You don't have enough coins. Don't try to break me :smirk:")

    """
    Error Handlers
    """

    # Beg command error handler
    @beg.error
    async def beg_error(self, ctx, error):
        # if on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            cdEmbed = discord.Embed(title = f"Slow it down bro!", description = f"Try again in {error.retry_after:.2f}s.\nCooldown is of 20s", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
            await ctx.send(embed = cdEmbed)
        # other error
        else:
            errorEmbed = discord.Embed(title = "Command `beg` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    # Bet command error handler
    @bet.error
    async def bet_error(self, ctx, error):
        # if on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            cdEmbed = discord.Embed(title = f"Slow it down bro!", description = f"Try again in {error.retry_after:.2f}s.\nCooldown is of 20s", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
            await ctx.send(embed = cdEmbed)
        # other errors
        else:
            errorEmbed = discord.Embed(title = "Command `bet` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

def setup(client: commands.Bot):
    client.add_cog(Economy(client))