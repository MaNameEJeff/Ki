#Cog with all commands related to winston

import discord
from discord.ext import commands, tasks
import time

class winston(commands.Cog):

	def __init__(self, client):
		self.client = client

	#Runs when the cog is loaded
	@commands.Cog.listener()
	async def on_ready(self):
		self.checkWinstonStatus.start()

	#Checks if Winston is online or not. Run every hour.
	@tasks.loop(hours=1)
	async def checkWinstonStatus(self):
	
		await self.client.spawn_channel.send("Updating Winston's status...")
	
		#If winston is online update status
		if ((self.client.winston_status == False) and ((await self.client.command_channel.history(limit=1).flatten())[0].content == 'online')):
			self.client.winston_status = True
	
	#Restarts the checkWinstonStatus task. Used to update status immediately instead of waiting for an hour
	@commands.command()
	async def check_winston_status(self, ctx):
		self.checkWinstonStatus.restart()
		time.sleep(2)
	
		if (self.client.winston_status == True):
			await ctx.send("Winston is online")
		else:
			await ctx.send("Winston is offline")

	#Spam
	@commands.command()
	async def spam(self, ctx, number=5, text = "spam", is_session=False):
	
		#Spam only mentioned number of messages as it is not a session
		if((self.client.winston_status) and (is_session == False)):
			await ctx.send(f'Spamming {number} messages...')
			await self.client.spam_channel.send(str(number) + " " + text + " " + str(is_session))
	
		#Start a spam session
		elif((self.client.winston_status) and (is_session)):
			await ctx.send("Starting a session")
			await self.client.spam_channel.send(str(number) + " " + text + " " + str(is_session))
	
		else:
			await ctx.send('Sorry Winston seems to be offline...')
	
	#Stop Winston spamming
	@commands.command()
	async def stopSpam(self, ctx):
		await ctx.send("Stopping session")
		await self.client.command_channel.send("Stop Spam")
	
	#Handle invalid arguments in the spam command
	@spam.error
	async def spam_error(self, ctx, error):
		await ctx.send(f"{error} The syntax is spam[number, message, is_session]")

	#Close Muxus and winston
	@commands.command()
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