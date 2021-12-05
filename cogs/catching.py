#Decide what pokemon has spawned and who catches it

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord import Color
from cogs import shinyhunt
from cogs import automated
import random

class catching(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.shiny_hunt = shinyhunt.shinyhunt(self.client)
		self.automated_account = automated.automated(self.client)
		self.hint = ""

	#Take a hint from PokeTwo
	async def take_hint(self):

		#Function to check if message is from Poketwo
		def check(m):
			return m.author.id == self.client.poketwo_id

		await self.client.command_channel.send("Winston #pokemon-spawn Say ?h")
		message = await self.client.wait_for('message', check=check)

		self.hint = message.content.split(" ")[-1]
		self.hint = self.hint[:-1]
		self.hint = self.hint.replace("\\", "")

	#Find out what Pokemon it is by comparing the hint with the names of pokemon
	async def what_pokemon(self):

		possible_pokemon = []

		while True:

			await self.take_hint()
	
			for pokemon in self.client.pokemon_in_game:
				if(len(pokemon) == len(self.hint)):
					possible_pokemon.append(pokemon)
	
			letter_count = 0
			while(letter_count < len(self.hint)):
				if(self.hint[letter_count] != "_"):
					count = 0
					while (count < len(possible_pokemon)):
						if(possible_pokemon[count][letter_count] != self.hint[letter_count]):
							possible_pokemon.remove(possible_pokemon[count])
							count -= 1
						count += 1
				letter_count += 1

			#If there's more than one possibility take another hint
			if(len(possible_pokemon) > 1):
				continue
			break
		return possible_pokemon[0]

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

		#Check pokemon name with user's list of pokemon
		uncaught = []
		name = await self.what_pokemon()
		users = dict(self.client.data_base.db.child("users").get().val())
	
		for user, data in users.items():
			if(data["mention_if_no_list"] == "True"):
				button_text = "Don't Mention Me"
				text = f"<@{int(user)}>"
			else:
				button_text = "Mention Me"
				text = f"{data['name']}"

			try:
				if name in data["list"]:
					uncaught.append({"name": user, "id": data["id"]})
			except:
				await self.client.spawn_channel.send(f"{text} you haven't made a list yet!", components=[
                                    																	create_actionrow(
                                        																	create_button(style=ButtonStyle.green, label=button_text, custom_id="mention_user")
                                        																)
                                    																  ])
		#If somebody still has to catch it mention them and stop spam.
		if(len(uncaught) == 0):
			users_shiny_hunts = await self.is_being_shiny_hunted(name)

			#If the pokemon is being shiny hunted by someone mention them and stop spam
			if(len(users_shiny_hunts) == 0):
				#Otherwise ask an automated account to catch it
				chosen_slave = (random.choices(self.client.available_slaves, k=1))[0]
				await self.client.command_channel.send(f"{chosen_slave['name']} pokemon {name}")
				await self.automated_account.update_list(chosen_slave['name'], chosen_slave['master'])

			else:
				m = ""
				for user in users_shiny_hunts:
					m += f'<@{user["id"]}>' + ", "
	
				m = m[:-2]
				m += " you're shiny hunting this pokemon"

				await self.client.command_channel.send("Stop Spam")
				await self.client.spawn_channel.send(m)
				await self.client.spawn_channel.send("Session terminated")

		else:
			m = "Wait "
			for user in uncaught:
				m += f'<@{user["id"]}>' + ", "

			m = m[:-2]
			m += " need to catch this"

			await self.client.command_channel.send("Stop Spam")
			await self.client.spawn_channel.send(m)
			await self.client.spawn_channel.send("Session terminated")

		#Return the name of the pokemon as that Muxus can download the image
		return name

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

def setup(client):
	client.add_cog(catching(client))