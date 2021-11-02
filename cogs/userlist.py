#Cog with commands to manage the custom list of pokemon of user

import discord
from discord.ext import commands

class userlist(commands.Cog):

	def __init__(self, client):
		self.client = client

	#Makes list of Pokemon
	@commands.command()
	async def makeList(self, ctx):
	
		#Function to check if message is from Poketwo
		def check(m):
			return m.author.id == self.client.poketwo_id
	
		list_of_pokemon = []
		count = 0
	
		while (True):
	
			if(count == 0):
				await ctx.send('Open list of pokemon')
			else:
				await ctx.send('Go to next page')
	
			#Get message from discord and check if it is from Poketwo
			message = await self.client.wait_for('message', check=check)
	
			#Get embeds from message
			message_content = (message.embeds[0]).to_dict()
	
			#Get the number of Pokemon from footer
			if(count == 0):
				number_of_pokemon_string = (((message_content.get('footer')).get('text')).split(' '))[-1]
				number_of_pokemon = int(number_of_pokemon_string[:-1])
	
			#Get the names of pokemon and append them to list_of_pokemon
			list_of_embeds = message_content.get('fields')
			list_of_embeds.pop(-1)
	
			for embed in list_of_embeds:
				list_of_pokemon.append((embed.get('name')).split(" ")[1])	

			count += 1
	
			#If count is greater than number of pages in list, stop
			if(count > int(number_of_pokemon/20)):
				break
	
		#Save user's list in respective channel
		channel = self.client.ki_users.get(ctx.author.id)
		for i in list_of_pokemon:
			await channel.send(i)
	
		await ctx.send(f'{ctx.author.name}, your list of pokemon is successfully stored')	

	#Clears user's list
	@commands.command()
	async def clearList(self, ctx):
	
		await ctx.send("Clearing list...")
	
		#Clear respective user's saved list
		channel = self.client.ki_users.get(ctx.author.id)
		await channel.purge(limit=1000)
		await ctx.send(f'{ctx.author.name} your list is cleared')
	
	#Shows user's saved list of pokemon_spawn_message					
	@commands.command()
	async def showList(self, ctx):
		
		channel = self.client.ki_users.get(ctx.author.id)
		messages = await channel.history(limit = 1000).flatten()
	
		if(len(l) == 0):
			await ctx.send("list is empty")
			return
	
		#Send each pokemon name as a seperate message
		for message in messages:
			await ctx.send(message.content)

def setup(client):
	client.add_cog(userlist(client))