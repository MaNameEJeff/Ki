import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from AutomatedAccount import AutomatedAccount

client = commands.Bot(command_prefix = '?')

#Load env file to retrieve token, email and password
load_dotenv('.env')
krenko = AutomatedAccount()

@client.event
async def on_ready():
	global pokemon_channel, spam_channel, command_channel, Ki_id

	#Initialize global variables
	for text_channel in client.guilds[0].text_channels:
		if(text_channel.id == 881875552028483594):
			pokemon_channel = text_channel
		elif(text_channel.id == 882583920963625010):
			spam_channel = text_channel
		elif(text_channel.id == 882872744323203072):
			command_channel = text_channel

	Ki_id = 790492561348886570

	await command_channel.send("online")
	print('Ready to serve')

@client.event
async def on_message(message):

	#Check if message is from Ki and if it is a command
	if ((message.author.id == Ki_id) and (message.channel.id == command_channel.id)):
		if(message.content == 'Leave'):
			await leave()

	#Check if message is from Ki and if it is a pokemon name
	if ((message.author.id == Ki_id) and (message.channel.id == pokemon_channel.id)):
		name = (await pokemon_channel.history(limit=1).flatten())[0].content

		#Ask krenko to catch the pokemon
		krenko.changeChannel('#pokemon-spawn')
		krenko.say('?c ' + name, krenko)

	#Check if message is from Ki and if it is a spam command
	if ((message.author.id == Ki_id) and (message.channel.id == spam_channel.id)):
		l = (await spam_channel.history(limit=1).flatten())[0].content
		count = (l.split(' '))[0]
		message = (l.split(' '))[1]

		#Ask krenko to spam
		krenko.changeChannel('#spam')
		krenko.rate_limited = False

		for i in range(int(count)):

			if(krenko.rate_limited == True):
				await command_channel.send('Rate Limited')
				return
				
			krenko.say(message, krenko)

#Close krenko and self
async def leave():
	krenko.close()
	await client.close()

#Run the bot
client.run(os.getenv('MUXUSTOKEN'))