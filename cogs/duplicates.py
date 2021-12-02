import discord
from discord.ext import commands
from discord_slash import cog_ext
import time

class duplicates(commands.Cog):

	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client
		self.trade_message_id = None
		self.trader_id = None

	@cog_ext.cog_slash(	name="remove_duplicates",
						guild_ids=server_ids,
						description="Removes duplicate Pokemon",
					  )

	async def remove_duplicates(self, ctx):

		if(self.client.winston_status == False):
			await ctx.send("Sorry all accounts seem to be offline")
			return

		await ctx.send(f"Check #{self.client.bot_channel}")
		await self.initiate_trade(ctx.author)

	async def get_pokemon_traded(self):
		#Function to check if message is from user
		def check(m):
			return m.author.id == self.trader_id

		#Function to check if message is from user
		def checkP2(m):
			return m.author.id == self.client.poketwo_id

		added = False
		while(added == False):
			pokemon_added_message = await self.client.wait_for('message', check=check)
			if("?t add" in pokemon_added_message.content):
				added = True
			else:
				await self.client.bot_channel.send(f"<@{self.trader_id}> add the pokemon to trade...")

		pokemon_traded = await self.client.wait_for('message', check=checkP2)
		
		while True:
			if("You can't trade" in pokemon_traded.content):
				pokemon_traded = await self.client.wait_for('message', check=checkP2)
			else:
				break

		pages = (pokemon_traded.embeds[0].to_dict())["footer"]["text"]

		pages = int(pages[pages.rindex(" ")+1:len(pages)-1])
		pokemon = []

		for page in range(1, pages+1):
			trade_data = (pokemon_traded.embeds[0].to_dict())["fields"][1]["value"]
			trade_data = trade_data.split("**")
			for td in range(1, len(trade_data), 2):
				pokemon.append(trade_data[td])
			await self.client.command_channel.send("Say ?n")
			pokemon_traded = await self.client.wait_for('message', check=checkP2)

		print(pokemon)
		print(len(pokemon))

		pokemon = set(pokemon)
		print(pokemon)
		print(len(pokemon))

	async def initiate_trade(self, user):

		#Function to check if message is from user
		def check(m):
			return m.author.id == user.id
		#Function to check if message is from user
		def checkP2(m):
			return m.author.id == self.client.poketwo_id

		self.trader_id = user.id

		await self.client.bot_channel.send("How many Pokemon do you want to check?")
		message = await self.client.wait_for('message', check=check)

		try:
			number_of_pokemon_to_check = int(message.content)
		except ValueError:
			await self.client.bot_channel.send("Not a valid number")
			return

		number_of_pokemon = ""
		for i in range(number_of_pokemon_to_check):
			number_of_pokemon += str(i+1) + " "

		i = 0
		while(i+2000 < len(number_of_pokemon)):
			await self.client.bot_channel.send(number_of_pokemon[i:i+2000])
			i += 2000
		await self.client.bot_channel.send(number_of_pokemon[i:])

		await self.client.command_channel.send(f"Say ?t <@{user.id}>")

		trade_message = await self.client.wait_for('message', check=checkP2)
		self.trade_message_id = trade_message.id

		await self.get_pokemon_traded()

		confirm_trade_message = await self.client.wait_for('message', check=check)
		if("?t c" in confirm_trade_message.content):
			await self.client.command_channel.send("Say ?t c")
		
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if((reaction.message.id == self.trade_message_id) and (reaction.message.author.id == self.trader_id)):
			await self.trade_message.add_reaction("✅")

def setup(client):
	client.add_cog(duplicates(client))