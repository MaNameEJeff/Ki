import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import random
import os
import time
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
	client.jeff_id = 730023436939952139
	client.spex_id = 729997258656972820
	client.poketwo_id = 716390085896962058
	client.guild_ids=[836276013830635590, 760880935557398608]

	client.ki_users = {client.moto_id: client.motolist, client.jeff_id: client.jefflist, client.spex_id: client.spexlist}
	client.winston_status = False

	print('ready')

#Custom Help command
#@client.command()
#async def help(ctx):
#
#	e = discord.Embed()
#	e.set_author(name='Help')
#	e.add_field(name='.makeList', value='Makes list of shown pokemon', inline=False)
#	e.add_field(name='.clearList', value='Clears user\'s list of pokemon', inline=False)
#	e.add_field(name='.showList', value='Shows user\'s list of pokemon', inline=False)
#	e.add_field(name='.numbers(start, stop)', value='Sends numbers from start till end', inline=False)
#	e.add_field(name='.spam(number of messages [default = 5], message [default = \'spam\'], is_session [default = False])', value='Spam', inline=False)
#	e.add_field(name='.stopSpam', value='Stops spam', inline=False)
#	e.add_field(name='.stopWinston', value='Stops Winston', inline=False)
#	e.add_field(name='.getImages(Number of messages to check, channel id) *Can only be used by MaNameEJeff', value='Gets images from the number of messages specified in channel', inline=False)
#	e.add_field(name='.check_winston_status', value='Checks if winston is online. By default runs every hour but can be restarted using this command', inline=False)
#
#	await ctx.send(embed = e)

##Handle the command not found exception
#@client.event
#async def on_command_error(ctx, error):
#	if(isinstance(error, commands.CommandNotFound)):
#		await ctx.send(f"{error}, for a list of commands type \".help\"")

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
			if ((pokemon_spawn_message.to_dict().get('title') == 'A wild pokémon has appeared!') or ('A new wild pokémon has appeared!' in pokemon_spawn_message.to_dict().get('title'))):
	
				#Get URL from image
				pokemon_URL = pokemon_spawn_message.image.url
	
				#Image recognition
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


#@slash.slash(name="test",
#             description="This is just a test command, nothing more.",
#             guild_ids=[836276013830635590, 760880935557398608],
#             options=[
#               create_option(
#                 name="optone",
#                 description="This is the first option we have.",
#                 option_type=3,
#                 required=True,
#                 choices=[
#                  create_choice(
#                    name="ChoiceOne",
#                    value="DOGE!"
#                  ),
#                  create_choice(
#                    name="ChoiceTwo",
#                    value="NO DOGE"
#                  )
#                ]
#               )
#             ])
#async def test(ctx, optone: str):
#  await ctx.send(content=f"Wow, you actually chose!@ {optone}? :(")

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
)

async def numbers(ctx:SlashContext, start, end):
	s = ""
	start = int(start)
	end = int(end)

	if(end < start):
		for i in range(int(start), int(end)-1, -1):
			s = s + str(i) + " "
	else:
		for i in range(int(start), int(end)+1):
			s = s + str(i) + " "

	await ctx.send(s)

#Load all cogs in cogs folder
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

#Run the bot
client.run("NzkwNDkyNTYxMzQ4ODg2NTcw.X-BZkQ.Ky_MKMB5hxr7ZDQYQQBDVPwHJoo")#os.environ['TOKEN'])