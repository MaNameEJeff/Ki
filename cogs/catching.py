import discord
from discord.ext import commands
from discord_slash import cog_ext
from cogs import shinyhunt
import random

class catching(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.shiny_hunt = shinyhunt.shinyhunt(self.client)
		self.hint = ""

	async def take_hint(self):

		#Function to check if message is from Poketwo
		def check(m):
			return m.author.id == self.client.poketwo_id

		await self.client.command_channel.send("Hint")
		message = await self.client.wait_for('message', check=check)

		self.hint = message.content.split(" ")[-1]
		self.hint = self.hint[:-1]
		self.hint = self.hint.replace("\\", "")

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

			if(len(possible_pokemon) > 1):
				continue
			break
		return possible_pokemon[0]

	async def is_being_shiny_hunted(self, name):

		shiny_hunts = []
		#shiny_hunt = shinyhunt.shinyhunt(self.client)

		is_a_shiny_hunt = await self.shiny_hunt.get_shinies()
		for user, shiny_pokemon in is_a_shiny_hunt.items():
			if(name == shiny_pokemon):
				shiny_hunts.append(user)

		return shiny_hunts

	async def who_catches(self):

		#Checks pokemon name with user's list of pokemon	
		pokemon = []
		uncaught = []
		name = await self.what_pokemon()
	
		for user_id, channel in self.client.ki_users.items():
			messages = await channel.history(limit = 1000, oldest_first = True).flatten() #Get user's saved list of pokemon
			for message in messages:
				message = message.embeds[0].to_dict()

				for pokemon_dict in message["fields"]:
					pokemon.append(pokemon_dict["value"])

			if name in pokemon:
				uncaught.append(user_id) #Save and return the users who haven't caught the pokemon
			pokemon = []

		if(len(uncaught) == 0):
			users_shiny_hunts = await self.is_being_shiny_hunted(name)

			if(len(users_shiny_hunts) == 0):
				await self.client.pokemon_names_channel.send(name)
			else:
				m = ""
				for user in users_shiny_hunts:
					m += f"<@{user}>" + ", "
	
				m = m[:-2]
				m += " you're shiny hunting this pokemon"

				await self.client.command_channel.send("Stop Spam")
				await self.client.spawn_channel.send(m)
				await self.client.spawn_channel.send("Session terminated")

		else:
			m = "Wait "
			for user in uncaught:
				m += f"<@{user}>" + ", "

			m = m[:-2]
			m += " need to catch this"

			await self.client.command_channel.send("Stop Spam")
			await self.client.spawn_channel.send(m)
			await self.client.spawn_channel.send("Session terminated")

		return name

def setup(client):
	client.add_cog(catching(client))