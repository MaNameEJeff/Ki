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

#Handle the command not found exception
@client.event
async def on_command_error(ctx, error):
	if(isinstance(error, commands.CommandNotFound)):
		await ctx.send(f"{error}, for a list of commands type \".help\"")
	else:
		await ctx.send(f"Error: {error}")

#Download images of pokemon in spawn channel
@client.command()
async def getImages(ctx, number_of_messages, channel_id):

	#Check if message author is Jeff or not
	if(ctx.author.id != jeff_id):
		await ctx.send('Only MaNameEJeff can use this')
		return

	#Check respective channel
	if (int(channel_id) == incense_channel.id):
		image_channel = incense_channel
	elif (int(channel_id) == spawn_channel.id):
		image_channel = spawn_channel

	#Get images and store them as a list in pokemon
	await ctx.send('Downloading images...')
	pokemon = await image_channel.history(limit=int(number_of_messages)).flatten()
	j = 0
	for message in pokemon:
		if(message.author.id != poketwo_id):
			continue
		try:
			#Check if it is a spawn message
			if ((message.embeds[0].to_dict()['title'] == 'A wild pokémon has appeared!') or ('A new wild pokémon has appeared!' in message.embeds[0].to_dict()['title'])):
	
				#Get URL from image
				pokemon_URL = message.embeds[0].image.url

				#Download image to specified path
				img_args = "wget -O {0} {1}".format('E:/Ki/Images/' + str(j) + '.jpg', pokemon_URL)
				j = j+1
				os.system(img_args)

		except IndexError:
			continue

	await ctx.send('Done')

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

#Makes List of Pokemon
@client.command()
async def makeList(ctx):

	#Function to check if message is from Poketwo
	def check(m):
		return m.author.id == poketwo_id

	list_of_pokemon = []
	count = 0

	while (True):

		if(count == 0):
			await ctx.send('Open list of pokemon')
		else:
			await ctx.send('Go to next page')

		#Get message from discord and check if it is from Poketwo
		message = await client.wait_for('message', check=check)

		#Get embeds from message
		message_content = message.embeds[0]

		#Get the number of Pokemon from footer
		if(count == 0):
			number_of_pokemon_string = ((((message_content.to_dict()['footer'])['text']).split(' '))[4])
			number_of_pokemon = int(number_of_pokemon_string[:number_of_pokemon_string.index('.')])

		#Get the names of pokemon and append them to list_of_pokemon
		list_of_embeds = message_content.to_dict()['fields']

		for i in range(len(list_of_embeds)-1):
			list_of_pokemon.append((list_of_embeds[i]['name'])[list_of_embeds[i]['name'].index(" "):list_of_embeds[i]['name'].index(" #")])		

		count += 1

		#If count is greater than number of pages in list stop
		if(count > int(number_of_pokemon/20)):
			break

	#Save user's list in respective channel
	channel = users.get(ctx.author.id)
	for i in list_of_pokemon:
		await channel.send(i)

	await ctx.send(f'{ctx.author.name}, your list of pokemon is successfully stored')	

#Clears user's list
@client.command()
async def clearList(ctx):

	await ctx.send("Clearing list...")

	#Clear respective user's saved list
	channel = users.get(ctx.author.id)
	await channel.purge(limit=1000)
	await ctx.send(f'{ctx.author.name} your list is cleared')

#Shows user's saved list of pokemon_spawn_message					
@client.command()
async def showList(ctx):
	
	channel = users.get(ctx.author.id)
	l = await channel.history(limit = 1000).flatten()

	if(len(l) == 0):
		await ctx.send("list is empty")
		return

	#Send each pokemon name as a seperate message
	for i in l:
		await ctx.send(i.content)
#Spam
@client.command()
async def spam(ctx, number=5, text = "spam", is_session=False):

	if(winston_status == False):
		await checkWinstonStatus()

	if((winston_status) and (is_session == False)):
		await ctx.send(f'Spamming {number} messages...')
		await spam_channel.send(str(number) + " " + text + str(is_session))

	elif((winston_status) and (is_session)):
		await ctx.send("Starting a session")
		await spam_channel.send(str(number) + " " + text + " " + str(is_session))

	else:
		await ctx.send('Sorry Winston seems to be offline...')

#Stop Winston spamming
@client.command()
async def stopSpam(ctx):
	await ctx.send("Stopping session")
	await command_channel.send("Stop Spam")

#Handle invalid arguments
@spam.error
async def spam_error(ctx, error):
	await ctx.send(f"{error} The syntax is spam[number, message, is_session]")

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

#Close Muxus
@client.command()
async def stopWinston(ctx):

	global winston_status

	#Check winston status and if he's offline exit
	if(winston_status == False):
		await checkWinstonStatus()

	if(winston_status == False):
		await ctx.send('Winston is already offline')
		return

	#Send prompt, clear messages in Winston's server and exit
	await ctx.send('Closing Winston')
	await command_channel.send('Leave')
	await command_channel.purge(limit=1000)
	await output_channel.purge(limit=1000)
	await spam_channel.purge(limit=1000)
	winston_status = False
	await ctx.send('Winston is now offline')

#Run the bot
client.run(os.environ['TOKEN'])