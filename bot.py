import discord
import pandas as pd
import openpyxl

from discord.ext import commands

df = pd.read_excel('test.xlsx')

def run_discord_bot():
    TOKEN = 'MTAzNzc2Njk2NDg2NjcyNzkzNg.G5fLZ4.Gu2igYMzoYHMfsSyYxeqK8GQyEFXi_T831pLYI'
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix = '/', intents=intents)
    f_read = open('whitelist.txt', 'r')
    original = f_read.readlines()
    id_lst = []
    print(df)
    for sub in original:
        id_lst.append(int(sub.replace("\n", "")))

    # rajouter le owner dessus
    # ajouter un timer pour combien de temps le bot run

    @client.command()
    async def list(ctx):
        global df
        print(df)

    @client.command()
    async def react(ctx):
        i = 1
        message = await ctx.send('Are you ready for christmas? \n')
        thumb_up = '👍'

        await message.add_reaction(thumb_up)

        def check(reaction, user):
            return str(reaction.emoji) in [thumb_up]
        
        try:
            found = 0
            reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)
            if str(reaction.emoji) == thumb_up:
                global df
                if user.id in df['id'].unique():
                    print("user already in list")
                else :
                    df = df.append(dict(zip(df.columns,[str(user.id), "123456789"])), ignore_index=True)
                    await user.send('Message de consentement')
        except  Exception as e:
            print(e)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await client.process_commands(message)
        if not isinstance(message.channel, discord.DMChannel):
            return
        global df
        user = message.author
        if not (user.id in df['id'].unique()):
            await user.send("Elle est où la thune?")
        else :
            user_message = str(message.content)
            print(user_message)
            #print(df.loc[df['id'] == user.id])
        #df = pandas.DataFrame()
        #df = df[df.text_column.str.contains(str(message.author.id))]

    #mettre un check si owner
    @client.command()
    async def shutdown(ctx):
        f_read.close()
        f_write = open('whitelist.txt', 'w')
        print("closing")
        for id in id_lst:
            print(str(id))
            f_write.write(str(id) + '\n')
        f_write.close()
        writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()
        await ctx.bot.close()


    client.run(TOKEN)