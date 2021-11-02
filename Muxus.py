import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from AutomatedAccount import AutomatedAccount
from datetime import datetime

client = commands.Bot(command_prefix = '?')

#Load env file to retrieve token, email and password
load_dotenv('.env')
krenko = AutomatedAccount()

@client.event
async def on_ready():

	#Initialize global variables
	for text_channel in client.guilds[0].text_channels:
		if(text_channel.id == 881875552028483594):
			client.pokemon_channel = text_channel
		elif(text_channel.id == 882583920963625010):
			client.spam_channel = text_channel
		elif(text_channel.id == 882872744323203072):
			client.command_channel = text_channel

	client.Ki_id = 790492561348886570
	client.spam_message = "spam"
	
	await client.command_channel.send("online")
	print('Ready to serve')

@client.event
async def on_message(message):

	#Check if message is from Ki and if it is a command
	if ((message.author.id == client.Ki_id) and (message.channel.id == client.command_channel.id)):
		if(message.content == 'Leave'):
			await leave()
		elif(message.content == 'Stop Spam'):
			spam.cancel()		

	#Check if message is from Ki and if it is a pokemon name
	if ((message.author.id == client.Ki_id) and (message.channel.id == client.pokemon_channel.id)):
		name = (await client.pokemon_channel.history(limit=1).flatten())[0].content
		spam.stop()

		#Ask krenko to catch the pokemon
		krenko.changeChannel('#pokemon-spawn')
		krenko.say('?c ' + name, krenko)
		krenko.changeChannel("#spam")
		spam.restart()

	#Check if message is from Ki and if it is a spam command
	if ((message.author.id == client.Ki_id) and (message.channel.id == client.spam_channel.id)):
		l = ((await client.spam_channel.history(limit=1).flatten())[0].content).split(" ")
		count = l[0]
		message = l[1]
		flag = l[2]
		krenko.changeChannel('#spam')
		krenko.rate_limited = False
		client.spam_message = message

		if(flag == "False"):
			for _ in range(int(count)):
				krenko.say(message, krenko)
			return

		#Ask krenko to spam
		spam.start()

#Start a background task of asking Winston to spam
@tasks.loop(seconds=3)
async def spam():

	if(krenko.rate_limited == True):
		await client.command_channel.send('Rate Limited')
		return
				
	krenko.say(client.spam_message, krenko)

#Close krenko and self
async def leave():
	krenko.close()
	await client.close()

#Run the bot
client.run(os.getenv('MUXUSTOKEN'))