#Cog with commands to manage the custom list of pokemon of user

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

class userlist(commands.Cog):

	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client

	#Manage User's list
	@cog_ext.cog_slash( name="mylist",
						guild_ids=server_ids,
						description="Manage my list of Pokemon",
						options=[
							create_option(
								name="manage",
								description="Manage my list",
								option_type=3,
								required=True,
								choices=[
									create_choice(
										name="Make my list",
										value="Make"
									),
									create_choice(
										name="Show my list",
										value="Show"
									),
									create_choice(
										name="Clear my list",
										value="Clear"
									)
								]
							)
						]
					  )
	async def mylist(self, ctx, manage: str):
		if(manage == "Make"):
			await self.makeList(ctx)
		elif(manage == "Show"):
			await self.showList(ctx)
		elif(manage == "Clear"):
			await self.clearList(ctx)

	#Makes list of Pokemon
	async def makeList(self, ctx):
	
		#Function to check if message is from Poketwo
		def check(m):
			return m.author.id == self.client.poketwo_id

		#Clear existing list
		self.client.data_base.db.child("users").child(ctx.author.id).child("list").remove()
	
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
				list_of_pokemon.append(embed.get('name')[embed.get('name').index(" "):embed.get('name').index("#")])	

			count += 1
	
			#If count is greater than number of pages in list, stop
			if(count > int(number_of_pokemon/20)):
				break
	
		count = 1
		list_data = {}

		#Store user's list in database
		for pokemon in list_of_pokemon:
			list_data[count] = pokemon.replace(" ", "")
			count += 1
	
		self.client.data_base.db.child("users").child(ctx.author.id).child("list").update(list_data)
		self.client.data_base.db.child("users").child(ctx.author.id).update({"name": ctx.author.name, "mention_if_no_list": "False"})
		await ctx.send(f'{ctx.author.name}, your list of pokemon is successfully stored')	

	#Clears user's list
	async def clearList(self, ctx):
	
		await ctx.send("Clearing list...")
	
		#Clear respective user's saved list
		self.client.data_base.db.child("users").child(ctx.author.id).child("list").remove()
		await ctx.send(f'{ctx.author.name} your list is cleared')
	
	#Shows user's saved list of Pokemon		
	async def showList(self, ctx):
		try:
			user_list = self.client.data_base.db.child("users").child(ctx.author.id).child("list").get().val()
			user_list.remove(None)
		except AttributeError:
			await ctx.send("List is empty")
			return

		pokemon_number = len(user_list)
		
		#Create the embeds and set the values
		pages = []

		#Set description based on whether the user is tracking his uncaught or not
		if(dict(self.client.data_base.db.child("users").child(ctx.author.id).get().val())["track_uncaught"] == "True"):
			description = 'Ki will mention you if a pokemon from this list spawns'
		else:
			description = '***Ki is not tracking your uncaught pokemon***. Use the /track command to start tracking'

		page = discord.Embed(title=f"**{ctx.author.name}'s List**", description=description)
		if(24 > len(user_list)):
			page.set_footer(text=f"Showing entries 1-{len(user_list)} out of {len(user_list)}")
		else:
			page.set_footer(text=f"Showing entries 1-24 out of {len(user_list)}")
		page.color = 0x7efb2a

		#Set the pokemon name values in embed considering the 25 field limit
		for pokemon_number in range(1, len(user_list)+1):
			if(pokemon_number % 25 == 0):
				pages.append(page)
				page = discord.Embed()

				if(pokemon_number+24 > len(user_list)):
					footer_text = f"{pokemon_number}-{len(user_list)}"
				else:
					footer_text = f"{pokemon_number}-{pokemon_number+24}"

				page.set_footer(text=f"Showing entries {footer_text} out of {len(user_list)}")
				page.color = 0x7efb2a
			page.add_field(name=pokemon_number, value=user_list[pokemon_number-1], inline=True)

		pages.append(page)

		#Display the list of embeds using the user menu
		await ctx.send(f"<@{ctx.author.id}> your list is")
		self.client.user_list_menu.set_data(data=pages)
		await self.client.user_list_menu.start(ctx)

	#Update user's list of pokemon
	async def update_list(self, user_id, pokemon):

		#Get original list
		user_list = self.client.data_base.db.child("users").child(user_id).child("list").get().val()
		self.client.data_base.db.child("users").child(user_id).child("list").remove()

		#Remove the caught pokemon
		user_list.remove(pokemon)

		#Convert list to dict and upload to database
		count = 1
		list_data = {}

		#Store user's list in database
		for pokemon in user_list:
			if(pokemon == None):
				continue
			list_data[count] = pokemon
			count += 1
		self.client.data_base.db.child("users").child(user_id).child("list").update(list_data)
			
def setup(client):
	client.add_cog(userlist(client))