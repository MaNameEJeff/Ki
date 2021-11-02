import discord
from discord.ext import commands
import random
import os
import time
import requests
import json

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

#Runs when Bot is ready
@client.event
async def on_ready():
	global spawn_channel, output_channel, motolist, spexlist, jefflist, spam_channel, command_channel, winston_status, incense_channel, users
	global moto_id, jeff_id, spex_id, poketwo_id

	#Initialize global variables
	for guild in client.guilds:
		if(guild.name == "Winston's server"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 882574195513516072):
					motolist = text_channel
				elif(text_channel.id == 882574240891666472):
					spexlist = text_channel
				elif(text_channel.id == 882574582924574770):
					jefflist = text_channel
				elif(text_channel.id == 881875552028483594):
					output_channel = text_channel
				elif(text_channel.id == 882583920963625010):
					spam_channel = text_channel
				elif(text_channel.id == 882872744323203072):
					command_channel = text_channel

		elif(guild.name == "The Bois"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 792314109625499668):
					spawn_channel = text_channel
				elif(text_channel.id == 851101277920559154):
					incense_channel = text_channel

	moto_id = 730020582393118730
	jeff_id = 730023436939952139
	spex_id = 729997258656972820
	poketwo_id = 716390085896962058

	users = {moto_id: motolist,
			jeff_id: jefflist,
			spex_id: spexlist}

	winston_status = False

	print('ready')

	client.var_spawn_channel = spawn_channel
	client.var_output_channel = output_channel
	client.var_spam_channel = spam_channel
	client.var_command_channel = command_channel
	client.var_incense_channel = incense_channel
	client.var_motolist = motolist
	client.var_spexlist = spexlist
	client.var_jefflist = jefflist
	client.var_winston_status = winston_status
	client.var_users = users
	client.var_moto_id = moto_id
	client.var_jeff_id = jeff_id
	client.var_spex_id = spex_id
	client.var_poketwo_id = poketwo_id


#Custom Help command
@client.command()
async def help(ctx):

	e = discord.Embed()
	e.set_author(name='Help')
	e.add_field(name='.makeList', value='Makes list of shown pokemon', inline=False)
	e.add_field(name='.clearList', value='Clears user\'s list of pokemon', inline=False)
	e.add_field(name='.showList', value='Shows user\'s list of pokemon', inline=False)
	e.add_field(name='.numbers(start, stop)', value='Sends numbers from start till end', inline=False)
	e.add_field(name='.spam(number of messages [default = 5], message [default = \'spam\'], is_session [default = False])', value='Spam', inline=False)
	e.add_field(name='.stopSpam', value='Stops spam', inline=False)
	e.add_field(name='.stopWinston', value='Stops Winston', inline=False)
	e.add_field(name='.getImages(Number of messages to check, channel id) *Can only be used by MaNameEJeff', value='Gets images from the number of messages specified in channel', inline=False)

	await ctx.send(embed = e)

#Checks if Winston is online or not
async def checkWinstonStatus():
	global winston_status
	if ((await command_channel.history(limit=1).flatten())[0].content == 'online'):
		winston_status = True
		client.var_winston_status = True

#Handle the command not found exception
@client.event
async def on_command_error(ctx, error):
	if(isinstance(error, commands.CommandNotFound)):
		await ctx.send(f"{error}, for a list of commands type \".help\"")
	else:
		await ctx.send(f"Error: {error}")

#Runs whenever a message is posted on Discord
@client.event
async def on_message(message):
	pokemon_names = []

	if(winston_status == False):
		await checkWinstonStatus()

	if((message.author.id == 882580519542468639) and (message.channel.id == command_channel.id) and (message.content == 'Rate Limited')):
		await spawn_channel.send("Winston is being rate limited right now... Try that again after a few seconds")
		await command_channel.purge(limit=1)
		return

	#Check to see if messsage if from poketwo in the spawn channel
	if((message.author.id == poketwo_id) and (message.channel.id == spawn_channel.id)):

		if(winston_status == False):
			return

		#Get the message from id
		pokemon_spawn_message = await message.channel.fetch_message(message.id)

		try:
			#Check if it is a spawn message
			if ((pokemon_spawn_message.embeds[0].to_dict()['title'] == 'A wild pokémon has appeared!') or ('A new wild pokémon has appeared!' in pokemon_spawn_message.embeds[0].to_dict()['title'])):
	
				#Get URL from image
				pokemon_URL = pokemon_spawn_message.embeds[0].image.url
	
				#Image recognition
				json_data = requests.post("http://pokemon-classifier-126641831.us-east-1.elb.amazonaws.com?image="+ pokemon_URL)
				json_list = json.loads(json_data.text)
				
				for i in range(len(json_list)):
					pokemon_names.append(json_list[i][0])
	
				#Check if pokemon is uncaught
				not_caught = await check(pokemon_names[0])

				#If everyone has caught it, ask winston to catch it
				if(len(not_caught) == 0):
					await output_channel.send(pokemon_names[0])
					return
				
				#Otherwise send prompt to catch the pokemon
				for name in not_caught:
					await message.channel.send(f"Wait <@{name}>, needs to catch this")

		except IndexError:
			return

	#Runs on_message alongside other commands
	await client.process_commands(message)

#Checks pokemon name with user's list of pokemon
async def check(name):

	channels = [moto_id, jeff_id, spex_id]
	pokemon = []
	uncaught = []

	for i in channels:
		messages = await users.get(i).history(limit=1000).flatten() #Get user's saved list of pokemon
		for message in messages:
			pokemon.append(message.content)
		if name in pokemon:
			uncaught.append(i) #Save and return the users who haven't caught the pokemon
		pokemon = []

	return uncaught

#Send numbers from start till end
@client.command()
async def numbers(ctx, start=0, end=0):
	s = ""

	if(end < start):
		for i in range(int(start), int(end)-1, -1):
			s = s + str(i) + " "
	else:
		for i in range(int(start), int(end)+1):
			s = s + str(i) + " "

	await ctx.send(s)

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")


#Run the bot
client.run("NzkwNDkyNTYxMzQ4ODg2NTcw.X-BZkQ.Ky_MKMB5hxr7ZDQYQQBDVPwHJoo")#os.environ['TOKEN'])