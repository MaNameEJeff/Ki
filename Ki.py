import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import os
import requests
import json

client = commands.Bot(command_prefix = '.')
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)

#Runs when Bot is ready
@client.event
async def on_ready():

	#Initialize Discord channels
	for guild in client.guilds:
		if(guild.name == "Winston's server"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 882574195513516072):
					client.motolist = text_channel
				elif(text_channel.id == 882574240891666472):
					client.spexlist = text_channel
				elif(text_channel.id == 882574582924574770):
					client.jefflist = text_channel
				elif(text_channel.id == 911646750547275816):
					client.gantherlist = text_channel
				elif(text_channel.id == 881875552028483594):
					client.pokemon_names_channel = text_channel
				elif(text_channel.id == 882583920963625010):
					client.spam_channel = text_channel
				elif(text_channel.id == 882872744323203072):
					client.command_channel = text_channel

		elif(guild.name == "The Bois"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 792314109625499668):
					client.spawn_channel = text_channel
				elif(text_channel.id == 851101277920559154):
					client.incense_channel = text_channel

	#Initialize ids
	client.moto_id = 730020582393118730
	client.ganther_id = 730028657581490176
	client.jeff_id = 730023436939952139
	client.spex_id = 729997258656972820
	client.poketwo_id = 716390085896962058

	client.winston_status = False

	client.ki_users = {
		client.moto_id: client.motolist,
		client.jeff_id: client.jefflist,
		client.spex_id: client.spexlist,
		client.ganther_id: client.gantherlist
	}

	print('ready')

#Runs whenever a message is posted on Discord
@client.event
async def on_message(message):

	#Check if Muxus says Winston is rate limited
	if((message.author.id == 882580519542468639) and (message.channel.id == client.command_channel.id) and (message.content == 'Rate Limited')):
		await client.spawn_channel.send("Winston is being rate limited right now... Try that again after a few seconds")
		await client.command_channel.purge(limit=1) #Remove the rate limited message afterwards
		return

	#Check to see if messsage if from poketwo in the spawn channel
	if((message.author.id == client.poketwo_id) and (message.channel.id == client.spawn_channel.id)):

		if(client.winston_status == False):
			return

		#Get the message from poketwo
		pokemon_spawn_message = (await message.channel.fetch_message(message.id)).embeds[0]

		try:
			#Check if it is a spawn message
			if ('wild pokémon has appeared!' in pokemon_spawn_message.to_dict().get('title')):
	
				#Get URL from image
				pokemon_URL = pokemon_spawn_message.image.url
	
				#Call Image recognition on AWS Rekognition model and get the json data
				json_data = requests.post("http://pokemon-classifier-126641831.us-east-1.elb.amazonaws.com?image="+ pokemon_URL)
				json_list = json.loads(json_data.text)
				pokemon_name = json_list[0][0]
	
				#Check if pokemon is uncaught
				not_caught = await check(pokemon_name)

				#If everyone has caught it, ask winston to catch it
				if(len(not_caught) == 0):
					await client.pokemon_names_channel.send(pokemon_name)
				
				else:				
					#Otherwise send prompt to catch the pokemon
					for name in not_caught:
						await message.channel.send(f"Wait <@{name}>, needs to catch this")

		except IndexError:
			return

	#Runs on_message alongside other commands
	await client.process_commands(message)

#Checks pokemon name with user's list of pokemon
async def check(name):

	pokemon = []
	uncaught = []

	for user_id, channel in client.ki_users.items():
		messages = await channel.history(limit=1000).flatten() #Get user's saved list of pokemon
		for message in messages:
			pokemon.append(message.content)
		if name in pokemon:
			uncaught.append(user_id) #Save and return the users who haven't caught the pokemon
		pokemon = []

	return uncaught

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

#Load all cogs in cogs folder
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

#Run the bot
client.run("NzkwNDkyNTYxMzQ4ODg2NTcw.X-BZkQ.IK9tetPdPDCBvaLxH0ZIheHM70s")#os.environ['TOKEN'])