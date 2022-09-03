#Cog with all commands related to automated accounts

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

import math
import random
import time

class automated(commands.Cog):

	#The servers in which the slash commands in this cog can be used
	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client

	#Checks if any automated accounts are online and if they are available
	@cog_ext.cog_slash( name="check_account_status",
						guild_ids=server_ids,
						description="Checks for any accounts that can be automated"
					  )
	async def check_account_status(self, ctx):

		#Get the accounts that are registered in database and store their ids
		try:
			automated_accounts = dict(self.client.data_base.db.child("automated").get().val())

		except TypeError:
			await ctx.send("No account is registered.")
			return

		account_ids = []
		for account in automated_accounts:
			account_ids.append(int(account))

		#Check their status on the Winston's server and if they're online append them to the available_slaves client attribute, along with the id of their master
		for guild in self.client.guilds:
			if(guild.name == "Winston's server"):
				for account_id in account_ids:
					if(str(guild.get_member(account_id).status) == "online"):
						automated_accounts[str(account_id)]["slave"]["master"] = account_id
						if(automated_accounts[str(account_id)]["slave"] not in self.client.available_slaves):
							self.client.available_slaves.append(automated_accounts[str(account_id)]["slave"])

		#Send confirmation
		if(len(self.client.available_slaves) == 0):
			await ctx.send("No account is online")
		else:
			names = []
			for slave in self.client.available_slaves:
				names.append(slave["name"])
			if(len(names) == 1):
				await ctx.send(names[0] + " is online")
			else:
				await ctx.send(", ".join(names) + " are online")
	#Spam
	@cog_ext.cog_slash(	name="spam",
						guild_ids=server_ids,
						description="Spam",
						options=[
							create_option(
								name="spam_tasks",
								description="Manage Accounts",
								option_type=3,
								required=True,
								choices=[
									create_choice(
										name="Stop Spam",
										value="Stop"
									),
									create_choice(
										name="Start Session",
										value="Session"
									),
									create_choice(
										name="Spam Messages",
										value="Spam"
									)
								]
							)
						]
					  )

	async def spam(self, ctx, spam_tasks):

		#Function to check if message is from the same user that issued the command
		def check(m):
			return ((m.channel == ctx.channel) and (m.author.id == ctx.author.id))

		if(len(self.client.available_slaves) == 0):
			await ctx.send('Sorry no account is online...')
			return
	
		#Spam only mentioned number of messages as it is not a session
		if(spam_tasks == "Spam"):

			await ctx.send("Enter the number of messages to send")
			number = (await self.client.wait_for('message', check=check)).content

			try:
				number = int(number)
			except ValueError:
				await ctx.send("Not a valid number")
				return

			await ctx.send("Enter the message to send")
			text = (await self.client.wait_for('message', check=check)).content

			chosen_slave = (random.choices(self.client.available_slaves, k=1))[0]

			await ctx.send(f'Spamming {number} messages...')
			await self.client.command_channel.send(f"{chosen_slave['name']} spam {number} {text} False")
	
		#Start a spam session
		elif(spam_tasks == "Session"):
			await ctx.send("Starting a session")

			await ctx.send("Enter the message to send")
			text = (await self.client.wait_for('message', check=check)).content

			for slave in self.client.available_slaves:
				await self.client.command_channel.send(f"{slave['name']} spam 1 {text} True")
	
		#Stop spamming
		elif(spam_tasks == "Stop"):
			await ctx.send("Stopping session")
			await self.client.command_channel.send("Stop Spam")
		
	#Stop a bot and respective slave account
	@cog_ext.cog_slash(	name="stopAccount",
						guild_ids=server_ids,
						description="Stops a running account",
						options=[
							create_option(
								name="account",
								description="Account to stop (NOT BOT NAME. Example:Winston). 'all' stops all running accounts",
								option_type=3,
								required=True
							)
						]
					  )

	async def stopAccount(self, ctx, account):

		account = account.capitalize()
		names = []
	
		if(len(self.client.available_slaves) == 0):
			await ctx.send('All accounts are already offline')
			return

		#Store the names of the slaves
		for slave in self.client.available_slaves:
			names.append(slave["name"])

		#Close all accounts and clear the command channel
		if(account == 'All'):
			await ctx.send('Closing all accounts...')
			for name in names:
				await self.client.command_channel.send(f'{name} Leave')
				time.sleep(1)
			self.client.available_slaves = []
			await ctx.send('All accounts are now offline. Discord may take a while to update status')

		#Close respective account
		else:
			if(account not in names):
				await ctx.send('That account is not registered')
				return
		
			#Send prompt, clear messages in Winston's server and exit
			await ctx.send(f'Closing {account}...')
			await self.client.command_channel.send(f'{account} Leave')
			
			for slave in self.client.available_slaves:
				if(slave["name"] == account):
					self.client.available_slaves.remove(slave)
			await ctx.send(f'{account} is now offline. Discord may take a while to update status')

		await self.client.command_channel.purge(limit=1000)

	#Get the pokemon that the account is shiny hunting along with the current streak
	async def get_automated_account_shiny(self, name, linked_main_account_id):
		
		#Function to check if message is from PokeTwo
		def checkP2(m):
			return m.author.id == self.client.poketwo_id

		#Get shiny hunt message
		await self.client.command_channel.send(f"{name} {self.client.spam_channel.id} Say <@{self.client.poketwo_id}> sh")
		shiny_message = await self.client.wait_for('message', check=checkP2)
		fields = shiny_message.embeds[0].to_dict()["fields"]
		shiny_hunt_data = {}

		#Try to get the shiny hunt data. If the account currently has no shiny hunt, return
		for field in fields:
			if(field["name"] == "Currently Hunting"):
				shiny_hunt_data["pokemon"] = field["value"]
			elif(field["name"] == "Chain"):
				shiny_hunt_data["streak"] = int(field["value"])

		#Store data in database
		self.client.data_base.db.child("automated").child(linked_main_account_id).child("slave").child("shiny").update(shiny_hunt_data)

	#Get the pokemon that the automated account has already caught and store them in the database
	async def get_pokemon(self, name, linked_main_account_id):

		#Function to check if message is from PokeTwo and in spam channel
		def checkP2(m):
			return ((m.author.id == self.client.poketwo_id) and (m.channel.name == "spam"))

		#Get the pokedex of account and get the number of pokemon
		await self.client.command_channel.send(f"{name} {self.client.spam_channel.id} Say <@{self.client.poketwo_id}> p")
		pokedex = await self.client.wait_for('message', check=checkP2)
		pokedex = pokedex.embeds[0].to_dict()
		number_of_pokemon = pokedex["footer"]["text"].split(" ")[-1]
		number_of_pokemon = int(number_of_pokemon[:-1])
		pokemon = []

		#Extract pokemon data and move to next page of pokedex if it exists
		for i in range(math.ceil(number_of_pokemon/20)):
			pokedex = pokedex["description"]
			pokedex = pokedex.split("\n")
			for pokemon_data in pokedex:
				current_pokemon = {
					"number": int(pokemon_data[pokemon_data.index("`")+1:pokemon_data.rindex("`")].replace(" ", "")),
					"name": pokemon_data[pokemon_data.index(">")+2:pokemon_data.rindex("*")-1],
					"level": pokemon_data[pokemon_data.index("•")+2:pokemon_data.rindex("•")-1],
					"iv": pokemon_data[pokemon_data.rindex("•")+2:]	
				}
				pokemon.append(current_pokemon)

			#If its the last page don't ask Winston to go to the next page
			if(i != math.ceil(number_of_pokemon/20)-1):
				await self.client.command_channel.send(f"{name} {self.client.spam_channel.id} Say <@{self.client.poketwo_id}> n")
				pokedex = await self.client.wait_for('message', check=checkP2)
				try:
					pokedex = pokedex.embeds[0].to_dict()
				except IndexError:

					#If menu has become unresponsive, open another menu and skip to the current page
					page = int(len(pokemon)/20)+1
					await self.client.command_channel.send(f"{name} {self.client.spam_channel.id} Say <@{self.client.poketwo_id}> p {page}")
					pokedex = await self.client.wait_for('message', check=checkP2)
					pokedex = pokedex.embeds[0].to_dict()

		#Store list in database
		for poke in pokemon:
			number = poke["number"]
			poke.pop("number") 
			self.client.data_base.db.child("automated").child(linked_main_account_id).child("slave").child("list").child(number).update(poke)

	#Register an account that can be automated in database
	@cog_ext.cog_slash(	name="addAccount",
						guild_ids=server_ids,
						description="Add another account which can be automated",
						options=[
							create_option(
								name="name",
								description="Name of the account that is to be automated",
								option_type=3,
								required=True
							),
							create_option(
								name="accountid",
								description="The id of the account that is to be automated",
								option_type=3,
								required=True
							),
							create_option(
								name="linked_main",
								description="The name of the main account to which this account is linked (BOT NAME)",
								option_type=3,
								required=True,
							),
							create_option(
								name="linked_main_account_id",
								description="The id of the main account to which this account is linked (BOT ID)",
								option_type=3,
								required=True
							)
						]
					  )
	async def addAccount(self, ctx, name, accountid, linked_main, linked_main_account_id):

		#Function to check if message is from PokeTwo
		def checkP2(m):
			return m.author.id == self.client.poketwo_id

		if((ctx.author.id not in self.client.authorized)):
			await ctx.send("You are not authorized to use this command")
			return

		name = name.capitalize()
		linked_main = linked_main.capitalize()

		#Store data in database
		self.client.data_base.db.child("automated").child(linked_main_account_id).update({"name": linked_main})
		self.client.data_base.db.child("automated").child(linked_main_account_id).child("slave").update({"name": name, "id": accountid})
		await ctx.send(f"{name} is now registered under {linked_main}")

		#Get the pokemon with the account
		await ctx.send("Storing the pokemon already on this account. This may take a while...")

		#Reindex the pokemon first
		await self.client.command_channel.send(f"{name} {ctx.channel.id} Say <@{self.client.poketwo_id}> reindex")
		while True:
			reindex_confirmation = await self.client.wait_for('message', check=checkP2)
			if(reindex_confirmation.content == "Successfully reindexed all your pokémon!"):
				break

		await self.get_pokemon(name, linked_main_account_id)

		#Get the shiny hunted pokemon of the account
		await ctx.send("Pokemon have been stored. Getting shiny data...")
		await self.get_automated_account_shiny(name, linked_main_account_id)

		await ctx.send(f"<@{ctx.author.id}> your account {name} can now be automated")

	#Update account list with pokemon caught
	async def update_list(self, catcher, linked_main_account_id):

		#Function to check if message is from PokeTwo and if it is in the spam channel
		def checkP2(m):
			return ((m.author.id == self.client.poketwo_id) and (m.channel.name == "spam"))

		#Get details of the pokemon caught
		await self.client.command_channel.send(f"{catcher} {self.client.spam_channel.id} Say <@{self.client.poketwo_id}> i l")
		pokemon_info = await self.client.wait_for('message', check=checkP2)
		pokemon_info = pokemon_info.embeds[0].to_dict()

		number = pokemon_info["footer"]["text"].split("\n")[0]
		number = number.split(" ")[-1]
		number = int(number[:-1])
		title = pokemon_info["title"].split(" ")

		poke = {
			"name": " ".join(title[2:]),
			"level": "Lvl. " + title[1]
		}

		pokemon_info = pokemon_info["fields"]
		for field in pokemon_info:
			if(field["name"] == "Stats"):
				poke["iv"] = field["value"][field["value"].rindex(" ")+1:]

		#Upload pokemon with details to database
		self.client.data_base.db.child("automated").child(linked_main_account_id).child("slave").child("list").child(number).update(poke)

	#Clear the existing pokemon list and store the updated one.
	#Use whenever large number of pokemon are removed from the automated account.
	#Single updates happen automatically
	@cog_ext.cog_slash(	name="restore_list",
						guild_ids=server_ids,
						description="Clears and stores the correct list of automated account on database.",
					  )
	async def restore_list(self, ctx=None, account_name=None, linked_main_account_id=None):

		names = []
		for slave in self.client.available_slaves:
			names.append(slave["name"])

		#If this is used as a slash command, perform some checks
		if(ctx != None):
			if((ctx.author.id not in self.client.authorized)):
				await ctx.send("You are not authorized to use this command")
				return

			if(account_name not in names):
				await ctx.send(f"{account_name} is not online")
				return

			await ctx.send("Storing the pokemon list again. This may take a while...")

		self.client.data_base.db.child("automated").child(linked_main_account_id).child("slave").child("list").remove()
		await self.get_pokemon(account_name, linked_main_account_id)
		await ctx.send("Finished")

def setup(client):
	client.add_cog(automated(client))