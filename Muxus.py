import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from AutomatedAccount import AutomatedAccount
import random
import time

client = commands.Bot(command_prefix = '?')

#Load env file to retrieve token, email and password
load_dotenv('.env')
krenko = AutomatedAccount()

@client.event
async def on_ready():

	#Initialize global variables
	for text_channel in client.guilds[0].text_channels:
		if(text_channel.id == 882872744323203072):
			client.command_channel = text_channel

	client.Ki_id = 790492561348886570
	client.spam_message = "spam"

	client.channel_ids = {
		"spawn": 792314109625499668,
		"spam": 890188908091039764
	}

	print('Ready to serve')

@client.event
async def on_message(message):

	#Check if message is from Ki and if it is a command
	if ((message.author.id == client.Ki_id) and (message.channel.id == client.command_channel.id)):
		command = message.content.split(" ")
		
		#Universal Commands
		if(" ".join(command) == 'Stop Spam'):
			spam.cancel()
		elif(command[0] == 'Download'):
			spam.cancel()
			await downloadImage(command[1], " ".join(command[2:]))

		#Winston Commands
		elif("Winston" == command[0]):
			if(command[1] == "pokemon"):
				pokemon_name = " ".join(command[2:])
				
				if(spam.is_running() == True):
					spam.stop()

				#Ask krenko to catch the pokemon
				if(krenko.current_channel != client.channel_ids["spawn"]):
					krenko.changeChannel(client.channel_ids["spawn"])

				krenko.say('?c ' + pokemon_name)

			elif(command[1] == 'Leave'):
				await leave()

			#Check if message is from Ki and if it is a spam command
			elif(command[1] == "spam"):

				count = command[2]
				m = command[3]
				flag = command[4]

				client.spam_message = m

				if(flag == "False"):
					for _ in range(int(count)):
						krenko.say(m)
				else:
					#Ask servants to spam
					if(spam.is_running() == True):
						spam.restart()
					else:
						spam.start()

			elif(command[2] == 'Say'):
				if(spam.is_running() == True):
					spam.stop()

				if(krenko.current_channel != int(command[1])):
					krenko.changeChannel(command[1])

				krenko.say(" ".join(command[3:]))

	#Runs on_message alongside other commands
	await client.process_commands(message)

async def downloadImage(URL, directory):

	if(directory == directory[:directory.rindex("/")] + "Type: Null"):
		directory = directory[:directory.rindex("/")] + "Type Null"

	#If image is of a nidoran variant, replace the symbols with text
	if("Nidoran" in directory):
		if("♀️" in directory):
			directory = directory[:directory.rindex("/")+1]+"NidoranFemale"
		else:
			directory = directory[:directory.rindex("/")+1]+"NidoranMale"

	folders = os.listdir(directory[:directory.rindex("/")])

	#Download the image
	for folder in folders:
		if (folder == directory[directory.rindex("/")+1:]):
			count = str(len(os.listdir(directory)) + 1)
			img_args = f"wget -O {directory}/{count}.png {URL}"
			os.system(img_args)

	if(spam.is_running() == True):
		spam.restart()
	else:
		spam.start()

#Start a background task of asking accounts to spam
@tasks.loop(seconds=2)
async def spam():

	if(krenko.current_channel != client.channel_ids["spam"]):
		krenko.changeChannel(client.channel_ids["spam"])

	if(krenko.rate_limited == True):
		await client.command_channel.send('Rate Limited')
		krenko.rate_limited = False
	else:
		krenko.say(client.spam_message)

#Close accounts and self
async def leave():
	krenko.close()
	await client.close()

#Run the bot
client.run(os.getenv('MUXUSTOKEN'))