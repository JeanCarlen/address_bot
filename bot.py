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
	df['name'] = df['name'].apply(str)
	df['address'] = df['address'].apply(str)
	df['code postal'] = df['code postal'].apply(str)
	df['city'] = df['city'].apply(str)
	df['pays'] = df['pays'].apply(str)
	print(df)

	# rajouter le owner dessus
	# ajouter un timer pour combien de temps le bot run

	@client.command()
	async def list(ctx):
		global df
		print(df)

	#@commands.is_owner()
	@client.command()
	async def explain(ctx):
		message = await ctx.send('Bonjour ! Je suis le bot des cartes postales. C’est moi qui récolte les informations des subs du mois de décembre pour que Mary puisse leur envoyer.  \n')

	#@commands.is_owner()
	@client.command()
	async def bot(ctx):
		message = await ctx.send('Bonjour c’est moi, je suis le bot des cartes postales et je suis en ligne ! Interagissez à ce message avec un “<3” si vous souhaitez que je vous envoie un message privé pour avoir vos informations pour la carte postale :)\n')
		thumb_up = '♥️'

		await message.add_reaction(thumb_up)

		def check(reaction, user):
			return str(reaction.emoji) in [thumb_up]
		while(1):
				try:
					reaction, user = await client.wait_for("reaction_add", timeout=0.5, check=check)
					if str(reaction.emoji) == thumb_up:
						global df
						print(user.id)
						if str(user.id) in df['id'].unique():
							await user.send('tu as déja donné tes infos, merci beaucoup! si tu as pas finis de remplir le questionnaire, écrit “recommencer”')
							print("user already in list")
						else :
							df = df.append(dict(zip(df.columns,[str(user.id)])), ignore_index=True)
							df['id'] = df['id'].apply(str)
							await user.send('Merci d’avoir réagit ! Enchanté. Je vais désormais te demander des informations pour avoir ton adresse postale pour que Mary puisse t’envoyer la carte postale. Sache que tes données sont sécurisés et ne seront pas utilisées pour autre chose que ceci. Es-tu d’accord ? Réponds “oui” pour continuer.')
				except  Exception as e:
					print(e)

	@client.event
	async def on_message(message):
		done = 0
		if message.author == client.user:
			return
		await client.process_commands(message)
		if not isinstance(message.channel, discord.DMChannel):
			return
		global df
		user = message.author
		if not (str(user.id) in df['id'].unique()):
			await user.send('Bonjour ! Tu n’as pas l’air d’être un sub Twitch de Mary, je ne peux donc pas te parler pour l’instant. As-tu pensé à lier ton compte discord à ton compte Twitch dans les options discord ? Le problème vient peut-être de la. Sinon, n’hésite pas à demander dans le channel d’aide du discord de Mary.')
		else :
			user_message = str(message.content)
			user_line = df.loc[df['id'] == str(user.id)]
			if (user_message.lower() == 'oui'):
				df.loc[df['id'] == str(user.id), 'consent'] = 'yes'
				await user.send("Super ! Quel est ton prénom ?")
			elif (user_line['consent'].item() == 'yes' and not user_line['locked'].item() == 'yes'):
				if (user_line['name'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'name'] = user_message
					await user.send("Noté. Quel est ton nom ?")
				elif (user_line['surname'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'surname'] = user_message
					await user.send("D’accord. Quelle est ton adresse maintenant ? (Le numéro de rue et la rue seulement. Exemple: 8 rue de la gare)")
				elif (user_line['address'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'address'] = user_message
					await user.send("Noté ! Maintenant, quel est ton code postal ? (Exemple: 75000)")
				elif (user_line['code postal'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'code postal'] = user_message
					await user.send(" Ok :) Bientôt fini. Quelle est ta ville maintenant ? (Exemple: Paris)")
				elif (user_line['city'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'city'] = user_message
					await user.send("Merci ! Dernière question, quel est ton pays ? (Exemple: France)")
				elif (user_line['pays'].isnull().values.any()):
					df.loc[df['id'] == str(user.id), 'pays'] = user_message
					await user.send("D’accord ! Je me permet de répeter ce que tu as dis juste pour vérifier que tout est correct. Tu m’as donné ces informations. écris “ok” pour continuer.")
				elif (user_line['locked'].isnull().values.any() and user_message.lower() == 'ok'):
					await user.send('nom et prénom => ' + user_line['name'].item() + " " + user_line['surname'].item())
					await user.send('adresse et code postal => ' + user_line['address'].item() + " " + user_line['code postal'].item())
					await user.send('ville et pays=> ' + user_line['city'].item() + " " + user_line['pays'].item())
					await user.send('Est ce que c’est bien correct (tu ne pourras pas changer ce que tu as dit)? Si c’est le cas réponds “accepter” sinon réponds moi “recommencer”')
				if (user_message.lower() == 'accepter'):
					df.loc[df['id'] == str(user.id), 'locked'] = 'yes'
					await user.send("Parfait ! Merci beaucoup ! Ton adresse a été notée. Bonne journée à toi !")
				if (user_message.lower() == 'recommencer' and not user_line['locked'].item() == 'yes'):
					df.loc[df['id'] == str(user.id), 'name'] = None
					df.loc[df['id'] == str(user.id), 'surname'] = None
					df.loc[df['id'] == str(user.id), 'address'] = None
					df.loc[df['id'] == str(user.id), 'code postal'] = None
					df.loc[df['id'] == str(user.id), 'city'] = None
					df.loc[df['id'] == str(user.id), 'pays'] = None
					await user.send("Recommençons ! Quel est ton prénom ?")
	#@commands.is_owner()
	@client.command()
	async def shutdown(ctx):
		writer = pd.ExcelWriter('test.xlsx', engine='openpyxl')
		df.to_excel(writer, sheet_name='Sheet1', index=False)
		writer.close()
		await ctx.bot.close()

	def print_data(user, user_line):
		global df
		user.send('Prénom =>' + user_line['name'].item())
		user.send('nom =>' + user_line['surname'].item())
		user.send('adresse =>' + user_line['address'].item())
		user.send('code postal =>' + user_line['code postal'].item())
		user.send('ville =>' + user_line['city'].item())

	client.run(TOKEN)