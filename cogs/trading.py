#Cog with commands to trade with any automated account

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import time
import math

class trading(commands.Cog):

	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client

	#List the pokemon that an automated account has caught in the wares channel
	@cog_ext.cog_slash( name="wares",
						guild_ids=server_ids,
						description="Show pokemon with account",
						options = [
							create_option(
								name="filters",
								description="The filters to be applied. If nothing is specified all pokemon are shown.",
								option_type=3,
								required=False
							),
							create_option(
								name="account",
								description="The account/s separated by ',', whose pokemon you want to view. Blank for all",
								option_type=3,
								required=False
							)
						]
	)
	async def wares(self, ctx, filters=None, account=None):

		#Check to see if message is from poketwo and is in the wares channel
		def checkP2(m):
			return ((m.author.id == self.client.poketwo_id) and (m.channel.id == self.client.wares_channel.id))

		if(len(self.client.available_slaves) == 0):
			await ctx.send("Sorry all accounts seem to be offline")
			return

		if(filters == None):
			filters = ""
		elif(filters.startswith("--") == False):
			await ctx.send("This filter is not supported by Poketwo")
			return

		merchants = []
		if(account == None):
			merchants = self.client.available_slaves
		else:
			for wanted in account.split(","):
				for slave in self.client.available_slaves:
					if(slave["name"] == wanted.capitalize()):
						merchants.append(slave)

		if(len(merchants) == 0):
			await ctx.send("That account is not registered yet or is not online")
			return

		await ctx.send(f"Displaying wares... Check <#{self.client.wares_channel.id}>")

		for merchant in merchants:
			await self.client.wares_channel.send(f"--------------------------------------------------{merchant['name']}'s Wares--------------------------------------------------")

			await self.client.command_channel.send(f"{merchant['name']} {self.client.wares_channel.id} Say ?p {filters}")
			message = await self.client.wait_for('message', check=checkP2)
			try:
				number_of_pokemon = message.embeds[0].to_dict()["footer"]["text"].split(" ")[-1]
				number_of_pokemon = number_of_pokemon[:-1]
				number_of_pokemon = int(number_of_pokemon)
				number_of_pages = math.ceil(number_of_pokemon/20)

				for page in range(1, number_of_pages):
					await self.client.command_channel.send(f"{merchant['name']} {self.client.wares_channel.id} Say ?n")
					await self.client.wait_for('message', check=checkP2)
			except IndexError:
				return

	@cog_ext.cog_slash(	name="trading",
						guild_ids=server_ids,
						description="Trade with any automated account",
						options = [
							create_option(
								name="transaction",
								description="The type of trade you want to initiate",
								option_type=3,
								required=True,
								choices=[
									create_choice(
										name="Trade pokemon for a better ones",
										value="better"
									),
									create_choice(
										name="Trade away any duplicates from given pokemon",
										value="duplicates"
									)
								]
							),
							create_option(
								name="account",
								description="The account you want to trade with",
								option_type=3,
								required=True
							)
						]
					  )

	async def trading(self, ctx, transaction=None, account=None):

		if(len(self.client.available_slaves) == False):
			await ctx.send("Sorry all accounts seem to be offline")
			return

		if(ctx.channel != self.client.bot_trade_channel):
			await ctx.send(f"You can only use this command in <#{self.client.bot_trade_channel.id}>")
			return

		valid_account_name = False

		for slave in self.client.available_slaves:
			if slave['name'] == account.capitalize():
				valid_account_name = True

		if(valid_account_name == False):
			await ctx.send(f"No account named {account} was found")
			return

		await ctx.send(f"Starting trade")

		is_confirmed = await self.initiate_trade(ctx.author, account.capitalize())
		if(is_confirmed == False):
			return

		pokemon_traded = await self.add_to_trade(ctx.author, account.capitalize())
		if(pokemon_traded == None):
			await ctx.send("No Pokemon traded...")
			await self.client.command_channel.send(f"{account.capitalize()} {self.client.bot_trade_channel.id} Say ?t x")
			return
		print(pokemon_traded)

#
#		if(transaction == "better"):
#			self.pokemon_to_return = self.replace_better_pokemon()
#		elif(transaction == "duplicates"):
#			await self.remove_duplicates()
#
#		if(self.pokemon_to_return == None):
#			await self.client.bot_trade_channel.send("No Pokemon To Trade")
#			return
#
#		await ctx.send("Done")
#
#		await self.initiate_trade(ctx.author, True)
#
#	#Function to check if message is from user
#	def checkP2(self, m):
#		return m.author.id == self.client.poketwo_id
	
	#Start the trade with user
	async def initiate_trade(self, user, account):

		#Check to see if message is from poketwo and is in the bot-trade channel
		def checkP2(m):
			return ((m.author.id == self.client.poketwo_id) and (m.channel.id == self.client.bot_trade_channel.id))

		#Ask the specified account to start the trade
		await self.client.command_channel.send(f"{account} {self.client.bot_trade_channel.id} Say ?t <@{user.id}>")
		confirm_trade_message = await self.client.wait_for('message', check=checkP2)

		#Ask the automated account to react to the trade confirming it
		await self.client.command_channel.send(f"{account} {self.client.bot_trade_channel.id} React {confirm_trade_message.id} white_check_mark")
		await self.client.bot_trade_channel.send(f"<@{user.id}> accept the trade")
		self.trade = await self.client.wait_for('message', check=checkP2)

		if(self.trade.content == "The request to trade has timed out."):
			return False
		else:
			return True

	async def add_to_trade(self, user, account, returning=False, pokemon_to_return=None):		
		
		#Function to check if message is from user and is in the bot-trade channel
		def check(m):
			return ((m.author.id == user.id) and (m.channel.id == self.client.bot_trade_channel.id))

		#Check to see if message is from poketwo and is in the bot-trade channel
		def checkP2(m):
			return ((m.author.id == self.client.poketwo_id) and (m.channel.id == self.client.bot_trade_channel.id))

		if(returning):
			await self.client.command_channel.send(f"{account} {self.client.bot_trade_channel.id} Say ?t add {' '.join(pokemon_to_return)}")
		else:
			await self.client.bot_trade_channel.send(f"<@{user.id}> add the pokemon")
			count = 0
			
			while True:
				message = await self.client.wait_for('message', check=check)
				if(("?t add" in message.content) or ("?trade add" in message.content) or (count > 4)):
					break
				count += 1

			if(count > 4):
				return None
			else:
				trade_message = await self.client.wait_for('message', check=checkP2)
				return(await self.get_pokemon_from_trade(trade_message.embeds[0].to_dict(), user.name, account))
#
#	async def complete_trade(self, user):
#
#		#Function to check if message is from user
#		def check(m):
#			return m.author.id == user.id
#
#		while True:
#			await self.client.bot_trade_channel.send(f"<@{user.id}> confirm trade")
#			message = await self.client.wait_for('message', check=check)
#			if(("?t c" in message.content) or ("?trade c" in message.content)):
#				await self.client.command_channel.send("Winston #bot-trade Say ?t c")
#				break


	async def get_pokemon_from_trade(self, trade_dict, trader_name, account):

		#Check to see if message is from poketwo and is in the bot-trade channel
		def checkP2(m):
			return ((m.author.id == self.client.poketwo_id) and (m.channel.id == self.client.bot_trade_channel.id))

		await self.client.bot_trade_channel.send("Getting data from trade...")
		pokemon = []
		number_of_pages = (trade_dict["footer"]["text"]).split(" ")[-1]
		number_of_pages = int(number_of_pages[:-1])

		for page in range(number_of_pages-1):
			for traders in trade_dict["fields"]:
				if(trader_name in traders["name"]):
					goods = traders["value"].replace("\n", "")
					pokemon_data = goods.split("%")
					pokemon_data.pop()
			
					for data in pokemon_data:
						pokemon.append({"name": data[data.index("**")+2:data.rindex("**")], "level": data[data.index("•")+1:data.rindex("•")], "iv": data[data.rindex("•")+1:] + "%"})

			await self.client.command_channel.send(f"{account} {self.client.bot_trade_channel.id} Say ?n")
			message = await self.client.wait_for('message', check=checkP2)
			trade_dict = message.embeds[0].to_dict()

		return pokemon

#	async def remove_duplicates(self):
#		pokemon_names = []
#		duplicates = []
#		for pokemon in self.pokemon_traded:
#			pokemon_names.append(pokemon["name"])
#
#		pokemon_names = set(pokemon_names)
#		pokemon_names = list(pokemon_names)
#
#		for pokemon in self.pokemon_traded:
#			if pokemon["name"] in pokemon_names:
#				pokemon_names.remove(pokemon["name"])
#				self.pokemon_to_return.append(pokemon)
#			else:
#				duplicates.append(pokemon)
#
#		await self.display_result(duplicates, "These pokemon were removed")
#
#	async def display_result(self, data, title):
#		result = []
#		page = discord.Embed(title=f"**{title}**")
#		pokemon_number = len(data)
#
#		if(pokemon_number+20 > len(data)):
#			page.set_footer(text=f"Showing entries 1-{len(data)} out of {len(data)}")
#		else:
#			page.set_footer(text=f"Showing entries 1-20 out of {len(data)}")
#		page.color = 0xb7ff00
#
#		#Set the pokemon name values in embed considering the 25 field limit
#		for pokemon_number in range(1, len(data)+1):
#			if(pokemon_number % 20 == 0):
#				result.append(page)
#				page = discord.Embed()
#
#				if(pokemon_number+20 > len(data)):
#					footer_text = f"{pokemon_number}-{len(data)}"
#				else:
#					footer_text = f"{pokemon_number}-{pokemon_number+20}"
#
#				page.set_footer(text=f"Showing entries {footer_text} out of {len(data)}")
#				page.color = 0xb7ff00
#			page.add_field(name=f"{data[pokemon_number-1]['name']}", value=f"{data[pokemon_number-1]['level']}　•　{data[pokemon_number-1]['iv']}", inline=False)
#
#		result.append(page)
#		self.client.user_list_menu.set_data(data=result)
#		await self.client.user_list_menu.start(self.context)
#
#	@commands.Cog.listener()
#	async def on_reaction_add(self, reaction, user):
#		try:
#			if((reaction.message.id == self.confirm_trade_message.id) and (reaction.message.author.id == user.id)):
#				await self.confirm_trade_message.add_reaction("✅")
#		except AttributeError:
#			return

def setup(client):
	client.add_cog(trading(client))