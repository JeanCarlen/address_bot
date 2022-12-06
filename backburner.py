    role1_id = 1038080407779934300
    guild1_id = 1028637243113480214
   
   
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
                    await message.user.send('Yes you can!')
                    return

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if (response != None):
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
            
            
    @client.event
    async def on_message(message):
        if message.content.startswith('$greet'):
            channel = message.channel
            await channel.send('Say hello!')

            def check(m):
                return m.content == 'hello' and m.channel == channel

            msg = await client.wait_for('message', check=check)
            await channel.send(f'Hello {msg.author}!')