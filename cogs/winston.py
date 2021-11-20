#Cog with all commands related to winston

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import time

class winston(commands.Cog):

	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client
	
	#Updates Winston's status
	@cog_ext.cog_slash( name="check_winston_status",
						guild_ids=server_ids,
						description="Updates winston's status"
					  )

	async def check_winston_status(self, ctx):

		status = (await self.client.command_channel.history(limit=1).flatten())[0].content
		if (status == "online"):
			await ctx.send("Winston is online")
			self.client.winston_status = True
		else:
			await ctx.send("Winston is offline")

	#Spam
	@cog_ext.cog_slash(	name="spam",
						guild_ids=server_ids,
						description="Spam",
						options=[
							create_option(
								name="spam_tasks",
								description="Manage Winston",
								option_type=3,
								required=True,
								choices=[
									create_choice(
										name="Stop Spam",
										value="Stop"
									),
									create_choice(
										name="Start Session",
										value="Session"
									),
									create_choice(
										name="Spam Messages",
										value="Spam"
									)
								]
							)
						]
					  )

	async def spam(self, ctx, spam_tasks):

		#Function to check if message is from Poketwo
		def check(m):
			return m.channel == ctx.channel

		if(self.client.winston_status == False):
			await ctx.send('Sorry Winston seems to be offline...')
			return
	
		#Spam only mentioned number of messages as it is not a session
		if(spam_tasks == "Spam"):

			await ctx.send("Enter the number of messages to send")
			number = (await self.client.wait_for('message', check=check)).content

			try:
				number = int(number)
			except ValueError:
				await ctx.send("Not a valid number")
				return

			await ctx.send("Enter the message to send")
			text = (await self.client.wait_for('message', check=check)).content

			await ctx.send(f'Spamming {number} messages...')
			await self.client.spam_channel.send(f"{number} {text} False")
	
		#Start a spam session
		elif(spam_tasks == "Session"):
			await ctx.send("Starting a session")

			await ctx.send("Enter the message to send")
			text = (await self.client.wait_for('message', check=check)).content

			await self.client.spam_channel.send(f"1 {text} True")
	
		#Stop Winston spamming
		elif(spam_tasks == "Stop"):
			await ctx.send("Stopping session")
			await self.client.command_channel.send("Stop Spam")
		
	#Close Muxus and winston
	@cog_ext.cog_slash(	name="stopWinston",
						guild_ids=server_ids,
						description="Stops Winston"
					  )

	async def stopWinston(self, ctx):
	
		if(self.client.winston_status == False):
			await ctx.send('Winston is already offline')
			return
	
		#Send prompt, clear messages in Winston's server and exit
		await ctx.send('Closing Winston')
		await self.client.command_channel.purge(limit=1000)
		await self.client.pokemon_names_channel.purge(limit=1000)
		await self.client.spam_channel.purge(limit=1000)
		await self.client.command_channel.send('Leave')
		self.client.winston_status = False
		await ctx.send('Winston is now offline')

def setup(client):
	client.add_cog(winston(client))