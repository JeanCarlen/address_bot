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
	df['id'] = df['id'].apply(str)
	print(df)

	# rajouter le owner dessus
	# ajouter un timer pour combien de temps le bot run

	@client.command()
	async def list(ctx):
		global df
		print(df)

	@client.command()
	async def react(ctx):
		message = await ctx.send('Are you ready for christmas? \n')
		thumb_up = '👍'

		await message.add_reaction(thumb_up)

		def check(reaction, user):
			return str(reaction.emoji) in [thumb_up]
		while(1):
				try:
					reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)
					if str(reaction.emoji) == thumb_up:
						global df
						print(user.id)
						if str(user.id) in df['id'].unique():
							print("user already in list")
						else :
							df = df.append(dict(zip(df.columns,[str(user.id)])), ignore_index=True)
							df['id'] = df['id'].apply(str)
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
		if not (str(user.id) in df['id'].unique()):
			await user.send("Elle est où la thune?")
		else :
			user_message = str(message.content)
			user_line = df.loc[df['id'] == str(user.id)]
			if (user_message.lower() == 'yes'):
				df.loc[df['id'] == str(user.id), 'consent'] = 'yes'
				await user.send("name?")
			elif (user_line['consent'].item() == 'yes'):
				print("are we in")
				if (user_line['name'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'name'] = user_message
					await user.send("surname?")
				elif (user_line['surname'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'surname'] = user_message
					await user.send("address?")
				elif (user_line['address'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'address'] = user_message
					await user.send("code postal")
				elif (user_line['code postal'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'code postal'] = user_message
					await user.send("city?")
				elif (user_line['city'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'city'] = user_message
					await user.send("country?")
				elif (user_line['country'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'country'] = user_message
					await user.send(df.loc[df['id'] == str(user.id)])

	#mettre un check si owner
	@client.command()
	async def shutdown(ctx):
		writer = pd.ExcelWriter('test.xlsx', engine='openpyxl')
		df.to_excel(writer, sheet_name='Sheet1', index=False)
		writer.close()
		await ctx.bot.close()


	client.run(TOKEN)