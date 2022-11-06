import discord
import responses
from discord.ext import commands

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if (response != None):
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTAzNzc2Njk2NDg2NjcyNzkzNg.G6WdqQ.OuQZ4jZUCWKVqKkCNXu7e5l1Q3tF0IUtBY6QdQ'
    role1_id = 1038080407779934300
    guild1_id = 1028637243113480214
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix = '/', intents=intents)
    file = open('whitelist.txt', "r")

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await client.process_commands(message)
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')
        
        if message.content.lower().startswith('can'):
            if message.guild:
                member = message.author
            else:  # private message
                guild = client.get_guild(guild1_id)
                member = await guild.fetch_member(message.author.id)
            #  only user with role1 is able to send the command
            for r in member.roles:
                if r.id == role1_id:
                    await message.channel.send('Yes you can!')
                    return
        
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
            
    @client.command()
    async def react(ctx):
        message = await ctx.send('Are you enjoying this bot? \n')

        thumb_up = '👍'

        await message.add_reaction(thumb_up)

        def check(reaction, user):
            return str(reaction.emoji) in [thumb_up]

        
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)
                if str(reaction.emoji) == thumb_up:
                    #for line in file.readlines():
                     #   if (line != user.id):
                      #      file.write(str(user.id) + '\n')
                       # else:
                        #    user.send("already in the list")
                    #await user.send('hello this is placeholder')
                    lines = file.readlines()
                    for line in lines:
                    # check if string present on a current line
                        if line.find(str(user.id)) != -1:
                            await user.send("already in the list")
            except  Exception as e:
                print(e)
            

    client.run(TOKEN)