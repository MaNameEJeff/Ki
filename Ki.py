import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import menus

import os
import time

from cogs import catching
from database import database
from UserListMenu import UserListMenu
from pokemon import pokemon

intents = discord.Intents.all()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix = '.', intents=intents)
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)

#Runs when Bot is ready
@client.event
async def on_ready():

	pokemon_obj = pokemon()
	client.pokemon_in_game = pokemon_obj.pokemon_in_game

	#Initialize Discord channels
	for guild in client.guilds:
		if(guild.name == "Winston's server"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 882872744323203072):
					client.command_channel = text_channel

		elif(guild.name == "The Bois"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 792314109625499668):
					client.spawn_channel = text_channel
				elif(text_channel.id == 850062129984831548):
					client.wares_channel = text_channel
				elif(text_channel.id == 916622948549410887):
					client.bot_trade_channel = text_channel
				elif(text_channel.id == 911663246673592320):
					client.karuta_channel = text_channel
				elif(text_channel.id == 890188908091039764):
					client.spam_channel = text_channel

	#Initialize ids
	client.poketwo_id = 716390085896962058

	client.available_slaves = []
	client.authorized = []

	#Initialize objects
	client.catch = catching.catching(client)
	client.data_base = database()
	client.user_list_menu = UserListMenu()

	#Authorized users who can add other accounts that can be automated
	for user, data in dict(client.data_base.db.child("users").get().val()).items():
		if((data["name"] == "MotoMoto") or (data["name"] == "MaNameEJeff")):
			client.authorized.append(int(user))

	print('ready')

#Runs whenever a message is posted on Discord
@client.event
async def on_message(message):

	#Check if Muxus says accounts are being rate limited
	if((message.author.id == 882580519542468639) and (message.channel.id == client.command_channel.id) and (message.content == 'Rate Limited')):
		await client.spawn_channel.send("Accounts are being rate limited right now... Try that again after a few seconds")
		await client.command_channel.purge(limit=1) #Remove the rate limited message afterwards
		return

	#Check to see if messsage if from poketwo in the spawn channel
	if((message.author.id == client.poketwo_id) and (message.channel.id == client.spawn_channel.id)):

		if(len(client.available_slaves) == 0):
			return

		try:

			#Get the message from poketwo
			pokemon_spawn_message = (await message.channel.fetch_message(message.id)).embeds[0]

			#Check if it is a spawn message
			if ('wild pokémon has appeared!' in pokemon_spawn_message.to_dict().get('title')):
								
				#Get URL and name of pokemon
				poke = await client.catch.who_catches()
				pokemon_URL = pokemon_spawn_message.image.url
				path = f"./Images/{poke}"

				#Ask Muxus to download it to directory
				await client.spawn_channel.send(f"Downloading image to {path}")
				await client.command_channel.send(f"Download {pokemon_URL} {path}")

		except IndexError:
			return

	#Runs on_message alongside other commands
	await client.process_commands(message)

#Send numbers from start till end
@slash.slash(
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
@slash.slash(
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
@slash.slash(
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

#Load all cogs in cogs folder
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

#Run the bot
client.run(os.environ['TOKEN'])