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

#Possible letters for typos
possible_typos = {
	'q' : ['w', 's', 'a',],
	'w' : ['q', 'e', 's',],
	'e' : ['w', 'r', 'd',],
	'r' : ['e', 't', 'f',],
	't' : ['r', 'y', 'g',],
	'y' : ['h', 't', 'u',],
	'u' : ['y', 'i', 'h',],
	'i' : ['k', 'o', 'u',],
	'o' : ['i', 'p', 'l',],
	'p' : ['o', '[', ';',],
	'a' : ['z', 'q', 's',],
	's' : ['w', 'a', 'd',],
	'd' : ['s', 'f', 'e',],
	'f' : ['r', 'g', 'd',],
	'g' : ['f', 'h', 't',],
	'h' : ['y', 'h', 'g',],
	'j' : ['h', 'i', 'l',],
	'k' : ['i', 'l', 'j',],
	'l' : ['k', ';', 'p',],
	'z' : ['a', 'x', 's',],
	'x' : ['c', 'z', 's',],
	'c' : ['x', 'v', 'd',],
	'v' : ['c', 'b', 'c',],
	'b' : ['v', 'n', 'h',],
	'n' : ['j', 'm', 'b',],
	'm' : ['n', ',', 'k',],
	':' : ["'", 'l', 'p'],
	"." : [',', '/', 'l'],
	"":[""], #For Nidoran♀ or Nidoran♂ if the typo function picks the emote it converts it to ""
	" ": [" "] #For white spaces in the name
}

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

				flag =  random.choices([True, False], weights = [0.8, 0.2], k=1)
				if (not flag[0]):
					await typo(pokemon_name)

				#Ask krenko to catch the pokemon
				if(krenko.current_channel != client.channel_ids["spawn"]):
					krenko.changeChannel(client.channel_ids["spawn"])

				krenko.say('?c ' + pokemon_name, clear_text_field=True)

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

				krenko.say(" ".join(command[3:]), clear_text_field=True)

			elif(command[2] == 'React'):
				if(spam.is_running() == True):
					spam.stop()

				if(krenko.current_channel != int(command[1])):
					krenko.changeChannel(command[1])

				krenko.addReaction(int(command[3]), command[4])

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

#Make a typo
async def typo(pokemon_name):

	pokemon_name = list(pokemon_name)

	number_of_errors = random.randrange(1, len(pokemon_name))
	altered_positions = []

	for _ in range(number_of_errors):

		while True:
			pos = random.randrange(0, len(pokemon_name))
			if(pos not in altered_positions):
				altered_positions.append(pos)
				break
				
		letter = pokemon_name[pos]
		wrong_letter = random.choice(possible_typos[letter.lower()])
		pokemon_name[pos] = wrong_letter

	pokemon_name = ''.join(pokemon_name)

	#Ask krenko to catch the pokemon
	if(krenko.current_channel != client.channel_ids["spawn"]):
		krenko.changeChannel(client.channel_ids["spawn"])

	krenko.say('?c ' + pokemon_name, clear_text_field=True)
	time.sleep(2)

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