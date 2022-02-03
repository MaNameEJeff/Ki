import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class random(commands.Cog):
	
	def __init__(self, client):
	 	self.client = client

	#Send numbers from start till end
	@cog_ext.cog_slash(
		name="numbers",
		description="Sends numbers from start till end",
		guild_ids=[760880935557398608],
		options=[
			create_option(
				name="start",
				description="Starting number",
				option_type=4,
				required=True
			),
			create_option(
				name="end",
				description="Ending number",
				option_type=4,
				required=True
			)
		]
	)

	async def numbers(ctx:SlashContext, start, end):
		s = ""

		if(end < start):
			for i in range(int(start), int(end)-1, -1):
				s += str(i) + " "
		else:
			for i in range(int(start), int(end)+1):
				s += str(i) + " "

		await ctx.send(s)

	#Get the cards codes from the lsit of cards that Karuta has sent
	@cog_ext.cog_slash(
		name="get_card_codes",
		description="Get the ids of the cards in a page in Karuta",
		guild_ids=[760880935557398608],
		options=[
			create_option(
				name="message_id",
				description="The id of the list of cards from Karuta",
				option_type=3,
				required=True
			)
		]
	)

	async def get_card_codes(ctx:SlashContext, message_id):

		#Check if the message id is a number
		try:
			message_id = int(message_id)
		except ValueError:
			await ctx.send("Wrong id")
			return

		#Check if the command was issued in the karuta channel or not
		if(int(ctx.channel.id) != client.karuta_channel.id):
			await ctx.send(f"This command cannot be used in this channel. Try using this command again in <#{client.karuta_channel.id}>")
			return

		#Get the message sent by Karuta, and get the card details from the embed
		karuta_message = ((await client.karuta_channel.fetch_message(message_id)).embeds[0]).to_dict()
		cards = karuta_message["description"][karuta_message["description"].index("\n")+2:]
		cards = cards.split("\n")
		
		#Get the codes from each card and store them in a list
		codes = []

		for card in cards:
			codes.append(f"**{card[card.index('`')+1:card.index('`', card.index('`')+1)]}**")

		#Output in the form of an embed
		output_embed = discord.Embed()
		output_embed.description = ", ".join(codes)
		await ctx.send(embed=output_embed)

	#Clear a number of messages from the channel in which command was issued
	@cog_ext.cog_slash(
		name="clear_messages",
		description="Clear a number of messages",
		guild_ids=[760880935557398608],
		options=[
			create_option(
				name="number",
				description="The number of messages to be cleared",
				option_type=4,
				required=True
			)
		]
	)
	async def clear_messages(ctx, number):
		await ctx.send(f"Clearing {number} messages...")
		time.sleep(1)
		await ctx.channel.purge(limit=number)


def setup(client):
	client.add_cog(random(client))