import discord, random, asyncio
from discord.ext import commands
from discord import Button, ActionRow


intents = discord.Intents.all()
colors = [0x0000EE, 0x00CD00, 0x05EDFF, 0x24D330, 0x5CACEE, 0x76EE00]
client = commands.Bot(command_prefix = "`", intents = intents, help_command = None, case_insensitive = True)

class Fun(commands.Cog, name="Fun"):
    @commands.command()
    async def infect(self, ctx, usr: discord.Member):
        win = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0]
        c = random.choice(win)
        if c == 0:
            await ctx.channel.send(f"Infected {usr}")
        else:
            await ctx.channel.send(f"Not infected {usr}")


    @commands.command()
    async def guess(self, ctx):
        await ctx.channel.send("Okay I have guessed a number between 0-10.\nYou have 3 chances to get it right!")
        answer = random.randint(0, 10)
        print(answer)

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        ans = False
        for i in range(3):
            try:
                guess = await client.wait_for('message', timeout = 10, check = is_correct)
            except asyncio.TimeoutError:
                await ctx.channel.send("You did not reply in time. So you lost <a:keka:807657992199733248>")
            if int(guess.content) == answer:
                ans = True
                break
            else:
                ans = False
            if ans:
                await ctx.channel.send(f"You guessed right!")
                break
            elif not ans:
                await ctx.channel.send(f"You guessed wrong")
        await ctx.channel.send(f"I had guessed {answer}")


    @commands.command()
    async def bon(self, ctx, tgt: discord.Member):
        await ctx.channel.purge(limit = 1)
        await ctx.channel.send(f"banned {tgt} <a:keka:807657992199733248>")



    @commands.command(aliases = ["8ball"])
    async def _8ball(self, ctx, *, question):
        global colors
        answers = [
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes – definitely',
            'You may rely on it',
            'As I see it, yes',
            'Most likely',
            'Outlook good',
            'Yes Signs point to yes',
            'Reply hazy',
            'try again',
            'Ask again later',
            'Better not tell you now',
            'Cannot predict now',
            'Concentrate and ask again',
            'Don\'t count on it',
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful'
        ]
        await ctx.send(f"You asked: {question}\n Here's what I think: {random.choice(answers)}")


    @commands.command()
    async def pressf(self, ctx, *, reason):
        global colors
        bann = await ctx.channel.send(f"{reason}. PAY RESPEKT BY REACTING TO <:f_:803555587077177374> ")
        await bann.add_reaction("<:f_:803555587077177374>")
        await asyncio.sleep(60)
        resp = await ctx.channel.fetch_message(bann.id)
        usrs = await resp.reactions[0].users().flatten()
        usrs.pop(usrs.index(client.user))
        for i in range(0, len(usrs)):
            await ctx.channel.send(f"**{usrs [i]}** has paid their repekts")



    # @commands.command()
    # async def rps(self, ctx, user: discord.Member):
    #     try:
    #         def check(message) -> bool:
    #             return user == message.author
    #         await ctx.send(f"**{ctx.author}** has challenged **{user}** for a ROCK, PAPER, SCISSOR MATCH!!!!!!!!!!!!!!!!!!!!!")
    #         await ctx.send(f"**{user}**, Reply with a ``yes`` or ``no`` to confirm your participation")
    #         message = await client.wait_for("message", timeout = 20, check = check)
    #
    #     except asyncio.TimeoutError:
    #         await ctx.send(f"**{user}** didnt reply what a nub.")
    #
    #     else:
    #         if message.content == "no":
    #             await ctx.send("Alright let's just pretend that never happened")
    #
    #         if message.content == "yes":
    #             player1 = ctx.author
    #             player2 = user
    #             await ctx.send("alright boys, Head over to your DMS")
    #             await player1.send("Choose now, ``stone`` or ``paper`` or ``scissors``?")
    #             try:
    #                 def player1_check(message) -> bool:
    #                     return player1 == message.author
    #                 player1_choice = await client.wait_for("message", timeout = 30, check = player1_check)
    #                 await player1.send(f"ok u chose {player1_choice.content}. Now waiting for {player2} to choose")
    #             except asyncio.TimeoutError:
    #                 await player1.send("You didnt reply in time nub.")
    #                 await ctx.send(f"{player1.mention} DIDNT REPLY SO HE IS A LOSER!, CONGRATS {player2.mention}, YOU WON!")
    #             else:
    #                 try:
    #                     def player2_check(message) -> bool:
    #                         return player2 == message.author
    #
    #                     await player2.send(f"Choose now, ``stone`` or ``paper`` or ``scissors``?")
    #                     player2_choice = await client.wait_for("message", timeout = 30, check = player2_check)
    #                     await player2.send(f"ok u chose {player2_choice.content} ")
    #                 except asyncio.TimeoutError:
    #                     await ctx.send(f"{player2.mention} DIDNT REPLY SO HE IS A LOSER!, CONGRATS {player1.mention}, YOU WON!")
    #                     await player2.send("LOSER")
    #                 else:
    #                     if player1_choice.content == player2_choice.content:
    #                         await ctx.send(f"ITS A TIE!!! {player1.mention} chose {player1_choice.content} and {player2.mention} chose {player2_choice.content}!!!")
    #                     if player1_choice == "stone":
    #                         if player2_choice.content == "scissors":
    #                             await ctx.send(f"GG! {player1.mention} chose {player1_choice.content}, which broke {player2.mention}'s {player2_choice.content}")
    #                         if player2_choice.content == "paper":
    #                             await ctx.send(f"GG! {player2.mention} chose {player2_choice.content}, which wrapped itself and got defeated  by {player1.mention}'s {player1_choice.content}")
    #                     if player1_choice.content == "paper":
    #                         if player2_choice.content == "scissors":
    #                             await ctx.send(f"GG! {player2.mention}'s {player2_choice.content} cut {player1.mention}'s {player1_choice.content}!")
    #                         elif player2_choice.content == "stone":
    #                             await ctx.send(f"GG! {player2.mention} chose {player2_choice.content}, which wrapped itself and got defeated by {player1.mention}'s {player1_choice.content}")
    #                     elif player1_choice.content == "scissors":
    #                         if player2_choice.content == "stone":
    #                             await ctx.send(
    #                                 f"GG! {player2.mention} chose {player2_choice.content}, which CRUSHED {player1.mention}'s {player1_choice.content}")
    #                         elif player2_choice.content == "paper":
    #                             await ctx.send(
    #                                 f"GG! {player1.mention} chose scissors got cut up {player2.mention}'s papers!")


    @commands.command()
    async def rps(self, ctx, user: discord.Member):
        try:
            # rpsChallengeEmbed = discord.Embed(title = f"{ctx.author.mention} has challenged {user.mention} for a rock-paper-scissor battle", description = f"{user.mention} click on 'Yes' button to accept the challenge or 'No' to deny the challenge.")
            # await ctx.send(embed=rpsChallengeEmbed, components=[Button(label="Yes"), Button(label="No")])
            # interaction = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("Yes"))
            # await interaction.respond(content = "idk what this does lul")
            components = [ActionRow(Button(label = 'Option Nr.1', custom_id = 'option1', emoji = "🆒", style = ButtonColor.green), Button(label = 'Option Nr.2', custom_id = 'option2', emoji = "🆗", style = ButtonColor.blurple)), ActionRow(Button(label = 'A Other Row', custom_id = 'sec_row_1st option', style = ButtonColor.red, emoji = '😀'), Button(url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', label = "This is an Link", emoji = '🎬'))]
            an_embed = discord.Embed(title = 'Here are some Button\'s', description = 'Choose an option', color = discord.Color.random())
            msg = await ctx.send(embed = an_embed, components = components)

        except asyncio.TimeoutError:
            await ctx.send(f"{user.mention} did not reply. What a nub.")


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
