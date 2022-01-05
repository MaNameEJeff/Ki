#Decide what pokemon has spawned and who catches it

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord import Color

from cogs import shinyhunt
from cogs import automated
from cogs import userlist

import random
import os
import time

class catching(commands.Cog):

	#The servers in which the slash commands in this cog can be used
	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client
		self.shiny_hunt = shinyhunt.shinyhunt(self.client)
		self.automated_account = automated.automated(self.client)
		self.user_list = userlist.userlist(self.client)
		self.hint = ""
		self.catcher_ids = []
		self.possible_pokemon = []

	#Take a hint from PokeTwo
	async def take_hint(self):

		#Function to check if message is from Poketwo
		def check(m):
			return m.author.id == self.client.poketwo_id

		chosen_slave = (random.choices(self.client.available_slaves, k=1))[0]

		await self.client.command_channel.send(f"{chosen_slave['name']} {self.client.spawn_channel.id} Say ?h")
		message = await self.client.wait_for('message', check=check)

		self.hint = message.content.split(" ")
		self.hint = self.hint[self.hint.index("is")+1:]
		self.hint[-1] = self.hint[-1][:-1]

		for word in self.hint:
			self.hint[self.hint.index(word)] = word.replace("\\", "")

	#Find out what Pokemon it is by comparing the hint with the names of pokemon
	async def what_pokemon(self):

		self.possible_pokemon = []
		type_of_pokemon = ""
		first_hint = True

		while True:

			await self.take_hint()

			#Check if the pokemon is Alolan or Galarian
			if(len(self.hint) > 1):
				if(len(self.hint[0]) == 6):
					type_of_pokemon = "Alolan "
				else:
					type_of_pokemon = "Galarian "
				self.hint = self.hint[1:]

			self.hint = " ".join(self.hint)
	
			if(first_hint):
				#Shorten the search to pokemon with the same number of letters as the hint
				for pokemon, attributes in self.client.pokemon_in_game.items():
					if(len(pokemon) == len(self.hint)):
						self.possible_pokemon.append(pokemon)
	
			#Find out what pokemon it is by comparing the letters shown in hint with the names of the pokemon
			letter_count = 0
			while(letter_count < len(self.hint)):
				if(self.hint[letter_count] != "_"):
					count = 0
					while (count < len(self.possible_pokemon)):
						if(self.possible_pokemon[count][letter_count] != self.hint[letter_count]):
							self.possible_pokemon.remove(self.possible_pokemon[count])
							count -= 1
						count += 1
				letter_count += 1

			#If there's more than one possibility take another hint and try again
			if(len(self.possible_pokemon) > 1):
				await self.client.spawn_channel.send(f"Found {len(self.possible_pokemon)} possible pokemon")
				await self.client.spawn_channel.send(", ".join(self.possible_pokemon))
				first_hint = False
				time.sleep(2)
				continue
			break

		return (type_of_pokemon + self.possible_pokemon[0])

	#Check if the pokemon is being shiny hunted
	async def is_being_shiny_hunted(self, name):

		shiny_hunts = []
		is_a_shiny_hunt = await self.shiny_hunt.get_shinies()

		if(is_a_shiny_hunt == None):
			return shiny_hunts

		for user_id, data in is_a_shiny_hunt.items():
			if(name == data["pokemon"]):
				shiny_hunts.append({"name": data["name"], "id": user_id})

		return shiny_hunts

	#Decide who catches the pokemon
	async def who_catches(self):

		#Function to check if message is from Poketwo
		def checkP2(m):
			return (m.author.id == self.client.poketwo_id)

		#Check pokemon name with user's list of pokemon
		uncaught = []
		name = await self.what_pokemon()
		users = dict(self.client.data_base.db.child("users").get().val())
	
		#Mention the user if they have no list. If they have specified otherwise, don't
		for user, data in users.items():
			if(data["mention_if_no_list"] == "True"):
				button_text = "Don't Mention Me"
				text = f"<@{int(user)}>"
			else:
				button_text = "Mention Me"
				text = f"{data['name']}"

			#If the pokemon is in user's list and if they want to track their uncaught pokemon, add them to the uncaught list
			try:
				if((name in data["list"]) and (data["track_uncaught"] == "True")):
					uncaught.append({"name": data["name"], "id": user})
			except:
				await self.client.spawn_channel.send(f"{text} you haven't made a list yet! Use the /mylist command to make one.", components=[
                                    																								create_actionrow(
                                        																								create_button(style=ButtonStyle.green, label=button_text, custom_id="mention_user")
                                        																							)
                                    																							  ])
		#If somebody still has to catch it mention them and stop spam.
		if(len(uncaught) == 0):
			users_shiny_hunts = await self.is_being_shiny_hunted(name)

			#If the pokemon is being shiny hunted by someone mention them and stop spam
			if(len(users_shiny_hunts) == 0):

				#Check if it is a shiny hunt of an automated account
				for master_id, master in dict(self.client.data_base.db.child("automated").get().val()).items():
					if(name == master["slave"]["shiny"]["pokemon"]):
						await self.client.command_channel.send(f"{master['slave']['name']} pokemon {name}")
						await self.shiny_hunt.update_streak(master["slave"]["id"], True)
						return

				#Otherwise ask a random account to catch it
				chosen_slave = (random.choices(self.client.available_slaves, k=1))[0]
				await self.client.command_channel.send(f"{chosen_slave['name']} pokemon {name}")
				await self.client.wait_for('message', check=checkP2)
				await self.automated_account.update_list(chosen_slave['name'], chosen_slave['master'])

			else:
				m = ""
				for user in users_shiny_hunts:
					m += f'<@{user["id"]}>' + ", "
					self.catcher_ids.append(int(user["id"]))
	
				m = m[:-2]
				m += " you're shiny hunting this pokemon"

				await self.client.command_channel.send("Stop Spam")
				await self.client.spawn_channel.send(m)
				await self.client.spawn_channel.send("Session terminated")
				await self.check_caught_message(name)

		else:
			m = "Wait "
			for user in uncaught:
				m += f'<@{user["id"]}>' + ", "
				self.catcher_ids.append(int(user["id"]))

			m = m[:-2]
			m += " need to catch this"

			await self.client.command_channel.send("Stop Spam")
			await self.client.spawn_channel.send(m, components=[
                                    					create_actionrow(
                                        					create_button(style=ButtonStyle.green, label="Don't Track My Uncaught Pokemon", custom_id="dont_track_uncaught")
                                        				)
                                    				  ])
			await self.client.spawn_channel.send("Session terminated")
			await self.check_caught_message(name)

		#Return the name of the pokemon as that Muxus can download the image
		return name

	#Get data from the caught message that PokeTwo sends and update lists respectively
	async def check_caught_message(self, name):

		#Function to check if message is from Poketwo
		def checkP2(m):
			return (m.author.id == self.client.poketwo_id)

		count=0

		#Return if caught message is found within 7 messages
		while True:
			caught_message = await self.client.wait_for('message', check=checkP2)
			caught_message = caught_message.content
			caught_message = caught_message.replace("!", "")
			caught_message = caught_message.replace("**", "")
			if(("Congratulations" in caught_message) or (count > 5)):
				break
			count += 1

		if(count>5):
			await self.client.spawn_channel.send("User data could not be updated automatically. [No caught message found]")
			return

		#Get the user who caught the pokemon and check if he/she was one of the users who HAD to catch it
		user_id = caught_message[caught_message.index("@")+1:caught_message.index(">")]
		user_id = int(user_id)

		if(user_id not in self.catcher_ids):
			await self.client.spawn_channel.send(f":upside_down:\n<@!{user_id}> why?")
			return

		#Update user list in database
		if("Shiny" in caught_message):
			streak = int(caught_message[caught_message.index("(")+1:caught_message.index(")")])
			await self.shiny_hunt.update_streak(user_id, streak)
			await self.client.spawn_channel.send(f"<@{user_id}> your streak has been updated")
		else:
			await self.user_list.update_list(user_id, name)
			await self.client.spawn_channel.send(f"<@{user_id}>, {name} has been removed from your list")

	#Toggle whether to mention the user if he has no list
	@cog_ext.cog_component()
	async def mention_user(self, ctx):
		users = dict(self.client.data_base.db.child("users").get().val())
		value = users[str(ctx.author.id)]["mention_if_no_list"]
		if(value == "True"):
			value = "False"
		else:
			value = "True"
		self.client.data_base.db.child("users").child(ctx.author.id).update({"mention_if_no_list": value})

		if(value == "False"):
			text = "not"
		else:
			text = ""
		await ctx.send(f"Ki will {text} mention you if you happen to have no list saved")

	#Stop tracking user's uncaught pokemon
	@cog_ext.cog_component()
	async def dont_track_uncaught(self, ctx):
		self.client.data_base.db.child("users").child(ctx.author.id).update({"track_uncaught": "False"})
		await ctx.send(f"Ki is not tracking your uncaught pokemon anymore <@{ctx.author.id}>.\n***Use the /track command to start tracking again***")

	#Start tracking user's uncaught pokemon again
	@cog_ext.cog_slash( name="track",
						guild_ids=server_ids,
						description="Start tracking uncaught pokemon"
					  )
	async def track(self, ctx):
		self.client.data_base.db.child("users").child(ctx.author.id).update({"track_uncaught": "True"})
		await ctx.send(f"Ki is now tracking your uncaught pokemon <@{ctx.author.id}>.")

def setup(client):
	client.add_cog(catching(client))