import discord, random, datetime
from discord.ext import commands

intents = discord.Intents.all()
colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]


class Moderation(commands.Cog, name='Moderation'):
    @commands.command(aliases = ["purge", "delete"], help = "Purge multiple messages")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amt: int = 1):
        await ctx.channel.purge(limit = amt + 1)
        purge = discord.Embed(title = "Command `;purge` => Success", colour = random.choice(colors))
        purge.add_field(name = "The command executed", value = f"Purged `{amt}` message(s)")
        await ctx.channel.send(embed = purge, delete_after = 5)

    @commands.command(help = "Kick members")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason = reason)
        kickEmbed = discord.Embed(title = f"{member} was kicked by {ctx.author}")
        await ctx.channel.send(embed=kickEmbed)

    @commands.command(help = "Ban members")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason = reason)
        banEmbed = discord.Embed(title = f"{member} was banned by {ctx.author}")
        await ctx.channel.send(embed=banEmbed)

    @commands.command(help = "Unban members")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        await member.unban(reason = reason)
        unbanEmbed = discord.Embed(title = f"{member} was unbanned by {ctx.author}")
        await ctx.channel.send(embed=unbanEmbed)

    @commands.command(help = "Change the name of the channel")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def editChannelName(self, ctx, *, name):
        await ctx.channel.edit(name=name)
        editEmbed = discord.Embed(title="command `*editChannelName` => success", description = f"The current channel name changed to {name}")
        await ctx.channel.send(embed=editEmbed)

    @commands.command(help = "Lock the channel.")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages or overwrite.send_messages is None:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            lockEmbed = discord.Embed(title = "Command `*lock` => executed")
            lockEmbed.add_field(name = "The command executed", value = f"{channel.mention} is now locked")
            await ctx.channel.send(embed = lockEmbed, delete_after = 5)
            await channel.send(embed = lockEmbed)
        else:
            lockEmbed = discord.Embed(title = "Command `lock` => unaffected")
            lockEmbed.add_field(name = "The command probably didn't work because:", value = "1. Channel is already unlocked")
            await ctx.channel.send(embed = lockEmbed, delete_after = 5)
            await channel.send(embed = lockEmbed)



    @commands.command(help = "Unlock the channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages:
            modem = discord.Embed(title="Command `unlock` => unaffected")
            modem.add_field(name="The command probably didn't work because:", value = "1. Channel is already unlocked")
            await ctx.channel.send(embed = modem, delete_after=5)
            await channel.send(embed = modem, delete_after=5)
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            modem = discord.Embed(title="Command `unlock` => Success")
            modem.add_field(name="The command executed", value = "The channel is now unlocked")
            await ctx.channel.send(embed= modem, delete_after=5)
            await channel.send(embed= modem, delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cdEmbed = discord.Embed(title = f"Slow it down bro!", description = f"Try again in {error.retry_after:.2f}s.\nCooldown is of 20s", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
            await ctx.send(embed = cdEmbed)
        elif isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `clear` => Fail", description = "You dont have permissions to delete messages")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `clear` => Fail", description = "The bot doesnt have permissions to delete messages")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `clear` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)


    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `unlock` => Fail", description = "You dont have permissions to manage channels")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `unlock` => Fail", description = "The bot doesnt have permissions to manage channels")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `unlock` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `lock` => Fail", description = "You dont have permissions to manage channels")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `lock` => Fail", description = "The bot doesnt have permissions to manage channels")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `lock` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    @editChannelName.error
    async def editChannelName_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cdEmbed = discord.Embed(title = f"Slow it down bro!", description = f"Try again in {error.retry_after:.2f}s.\nCooldown is of 20s", colour = random.choice(colors), timestamp = datetime.datetime.utcnow())
            await ctx.send(embed = cdEmbed)
        elif isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `editChannelName` => Fail", description = "You dont have permissions to manage channels")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `editChannelName` => Fail", description = "The bot doesnt have permissions to manage channels")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `editChannelName` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `ban` => Fail", description = "You dont have permissions to manage members")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.MemberNotFound):
            errorEmbed = discord.Embed(title = "Command => `ban` => Fail", description = "No such member found")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `ban` => Fail", description = "The bot doesnt have permissions to manage members")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `ban` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `unban` => Fail", description = "You dont have permissions to manage members")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.MemberNotFound):
            errorEmbed = discord.Embed(title = "Command => `unban` => Fail", description = "No such member found")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `unban` => Fail", description = "The bot doesnt have permissions to manage members")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `unban` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `kick` => Fail", description = "You dont have permissions to manage members")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.MemberNotFound):
            errorEmbed = discord.Embed(title = "Command => `kick` => Fail", description = "No such member found")
            await ctx.send(embed = errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title = "Command => `kick` => Fail", description = "The bot doesnt have permissions to manage members")
            await ctx.send(embed = errorEmbed)
        else:
            errorEmbed = discord.Embed(title = "Command `kick` => Fail", description = "Some error occurred")
            await ctx.channel.send(embed = errorEmbed)
            raise error

def setup(client: commands.Bot):
    client.add_cog(Moderation(client))