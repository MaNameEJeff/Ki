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
		self.confirm_trade_message = None
		self.trade = None
		self.pokemon_to_return = []
		self.pokemon_traded = []
		self.context = None

#	@cog_ext.cog_slash(	name="trading",
#						guild_ids=server_ids,
#						description="Trade with any automated account",
#						options = [
#							create_option(
#								name="transaction",
#								description="The type of trade you want to initiate",
#								option_type=3,
#								required=False,
#								choices=[
#									create_choice(
#										name="Trade pokemon for a better ones",
#										value="better"
#									),
#									create_choice(
#										name="Trade away any duplicates from given pokemon",
#										value="duplicates"
#									)
#								]
#							),
#							create_option(
#								name="wares",
#								description="Show Pokemon (All filters in PokeTwo are supported. 'all' will show all pokemon)",
#								option_type=3,
#								required=False,
#							)
#						]
#					  )
#
	async def trading(self, ctx, transaction=None, wares=None):

		if(len(self.client.available_slaves) == False):
			await ctx.send("Sorry all accounts seem to be offline")
			return

		if(ctx.channel != self.client.bot_trade_channel):
			await ctx.send(f"You can only use this command in <#{self.client.bot_trade_channel.id}>")
			return

		self.context = ctx
		await ctx.send("Starting trade")

		if(wares != None):
			await ctx.send(f"Check <#{self.client.wares_channel.id}>")
			await self.wares(wares)
			return

		await self.initiate_trade(ctx.author)

		if(transaction == "better"):
			self.pokemon_to_return = self.replace_better_pokemon()
		elif(transaction == "duplicates"):
			await self.remove_duplicates()

		if(self.pokemon_to_return == None):
			await self.client.bot_trade_channel.send("No Pokemon To Trade")
			return

		await ctx.send("Done")

		await self.initiate_trade(ctx.author, True)

	#Function to check if message is from user
	def checkP2(self, m):
		return m.author.id == self.client.poketwo_id

	async def initiate_trade(self, user, returning=False):
		await self.client.command_channel.send(f"Winston #bot-trade Say ?t <@{user.id}>")
		self.confirm_trade_message = await self.client.wait_for('message', check=self.checkP2)
		await self.add_to_trade(user, returning)

	async def add_to_trade(self, user, returning):		
		
		#Function to check if message is from user
		def check(m):
			return m.author.id == user.id

		if(returning):
			await self.client.command_channel.send(f"Winston #bot-trade Say ?t add {' '.join(self.pokemon_to_return)}")
		else:
			while True:
				await self.client.bot_trade_channel.send(f"<@{user.id}> add the pokemon")
				message = await self.client.wait_for('message', check=check)
				if(("?t add" in message.content) or ("?trade add" in message.content)):
					break

			trade_message = await self.client.wait_for('message', check=self.checkP2)
			self.pokemon_traded = await self.get_pokemon_from_trade(trade_message.embeds[0].to_dict(), user.name)

		await self.complete_trade(user)

	async def complete_trade(self, user):

		#Function to check if message is from user
		def check(m):
			return m.author.id == user.id

		while True:
			await self.client.bot_trade_channel.send(f"<@{user.id}> confirm trade")
			message = await self.client.wait_for('message', check=check)
			if(("?t c" in message.content) or ("?trade c" in message.content)):
				await self.client.command_channel.send("Winston #bot-trade Say ?t c")
				break


	async def get_pokemon_from_trade(self, trade_dict, trader_name):

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

			await self.client.command_channel.send("Winston #bot-trade Say ?n")
			message = await self.client.wait_for('message', check=self.checkP2)
			trade_dict = message.embeds[0].to_dict()

		return pokemon

	async def remove_duplicates(self):
		pokemon_names = []
		duplicates = []
		for pokemon in self.pokemon_traded:
			pokemon_names.append(pokemon["name"])

		pokemon_names = set(pokemon_names)
		pokemon_names = list(pokemon_names)

		for pokemon in self.pokemon_traded:
			if pokemon["name"] in pokemon_names:
				pokemon_names.remove(pokemon["name"])
				self.pokemon_to_return.append(pokemon)
			else:
				duplicates.append(pokemon)

		await self.display_result(duplicates, "These pokemon were removed")

	async def wares(self, filters):
		await self.client.wares_channel.send("-------------------------------------------------------------------------------------------------------")
		if(filters == "all"):
			filters = ""
		await self.client.command_channel.send(f"Winston #wares Say ?p {filters}")
		message = await self.client.wait_for('message', check=self.checkP2)
		try:
			number_of_pokemon = message.embeds[0].to_dict()["footer"]["text"].split(" ")[-1]
			number_of_pokemon = number_of_pokemon[:-1]
			number_of_pokemon = int(number_of_pokemon)
			number_of_pages = math.ceil(number_of_pokemon/20)

			for page in range(1, number_of_pages):
				await self.client.command_channel.send("Winston #wares Say ?n")
		except IndexError:
			return

	async def display_result(self, data, title):
		result = []
		page = discord.Embed(title=f"**{title}**")
		pokemon_number = len(data)

		if(pokemon_number+20 > len(data)):
			page.set_footer(text=f"Showing entries 1-{len(data)} out of {len(data)}")
		else:
			page.set_footer(text=f"Showing entries 1-20 out of {len(data)}")
		page.color = 0xb7ff00

		#Set the pokemon name values in embed considering the 25 field limit
		for pokemon_number in range(1, len(data)+1):
			if(pokemon_number % 20 == 0):
				result.append(page)
				page = discord.Embed()

				if(pokemon_number+20 > len(data)):
					footer_text = f"{pokemon_number}-{len(data)}"
				else:
					footer_text = f"{pokemon_number}-{pokemon_number+20}"

				page.set_footer(text=f"Showing entries {footer_text} out of {len(data)}")
				page.color = 0xb7ff00
			page.add_field(name=f"{data[pokemon_number-1]['name']}", value=f"{data[pokemon_number-1]['level']}　•　{data[pokemon_number-1]['iv']}", inline=False)

		result.append(page)
		self.client.user_list_menu.set_data(data=result)
		await self.client.user_list_menu.start(self.context)

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		try:
			if((reaction.message.id == self.confirm_trade_message.id) and (reaction.message.author.id == user.id)):
				await self.confirm_trade_message.add_reaction("✅")
		except AttributeError:
			return

def setup(client):
	client.add_cog(trading(client))