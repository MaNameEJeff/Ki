import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from AutomatedAccount import AutomatedAccount
import random

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
		elif((message.content.split(" "))[0] == 'Download'):
			spam.cancel()
			await downloadImage(message.content.split(" ")[1], " ".join(message.content.split(" ")[2:]))
		elif('Say' in message.content):
			krenko.changeChannel('#bot')
			krenko.say(message.content[4:])
		elif(message.content == 'Hint'):
			spam.stop()

			krenko.changeChannel('#pokemon-spawn')
			krenko.say("?h")
			krenko.changeChannel('#spam')

	#Check if message is from Ki and if it is a pokemon name
	if ((message.author.id == client.Ki_id) and (message.channel.id == client.pokemon_channel.id)):
		pokemon_name = (await client.pokemon_channel.history(limit=1).flatten())[0].content
		spam.stop()

		#Ask krenko to catch the pokemon
		krenko.changeChannel('#pokemon-spawn')
		krenko.say('?c ' + pokemon_name)
		krenko.changeChannel("#spam")
		spam.restart()

	#Check if message is from Ki and if it is a spam command
	if ((message.author.id == client.Ki_id) and (message.channel.id == client.spam_channel.id)):
		krenko.changeChannel("#spam")
		l = ((await client.spam_channel.history(limit=1).flatten())[0].content).split(" ")
		count = l[0]
		m = l[1]
		flag = l[2]

		client.spam_message = m

		if(flag == "False"):
			krenko.changeChannel("#spam")
			for _ in range(int(count)):
				krenko.say(m)
		else:
			#Ask servants to spam
			spam.start()

	#Runs on_message alongside other commands
	await client.process_commands(message)

async def downloadImage(URL, directory):

	if(directory == directory[:directory.rindex("/")] + "Type: Null"):
		directory = directory[:directory.rindex("/")] + "Type Null"

	folders = os.listdir(directory[:directory.rindex("/")])

	for folder in folders:
		if (folder == directory[directory.rindex("/")+1:]):
			#count = str(len(os.listdir(directory)) + 1)
			img_args = f"wget -O {directory}/0.png {URL}"
			os.system(img_args)

	#spam.start()

#Start a background task of asking accounts to spam
@tasks.loop(seconds=2)
async def spam():

	if(krenko.rate_limited == True):
		await client.command_channel.send('Rate Limited')
	else:
		krenko.say(client.spam_message)

#Close accounts and self
async def leave():
	krenko.close()
	await client.close()

#Run the bot
client.run(os.getenv('MUXUSTOKEN'))