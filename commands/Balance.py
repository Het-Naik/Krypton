import json
from discord.ext import commands

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


class Balance(commands.Cog, name='Balance'):

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        user = ctx.message.author
        await open_acc(user = user)
        acc_details = await bal_data()
        wal = acc_details[str(user.id)]["wallet"]
        bank = acc_details[str(user.id)]["bank"]
        await ctx.channel.send(f"Wallet: {wal}\nBank: {bank}")

def setup(client: commands.Bot):
    client.add_cog(Balance(client))