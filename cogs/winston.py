#Cog with all commands related to winston

import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext
import time

class winston(commands.Cog):

	server_ids = [836276013830635590, 760880935557398608]

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
	@cog_ext.cog_slash(name="check_winston_status", guild_ids=server_ids, description="Checks if winston is online. By default runs every hour but can be restarted using this command")
	async def check_winston_status(self, ctx):
		self.checkWinstonStatus.restart()
		time.sleep(2)
	
		if (self.client.winston_status == True):
			await ctx.send("Winston is online")
		else:
			await ctx.send("Winston is offline")

	#Spam
	@cog_ext.cog_slash(name="spam", guild_ids=server_ids, description="Spam")
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
	@cog_ext.cog_slash(name="stopSpam", guild_ids=server_ids, description="Stops spam")
	async def stopSpam(self, ctx):
		await ctx.send("Stopping session")
		await self.client.command_channel.send("Stop Spam")
	
	#Handle invalid arguments in the spam command
	@spam.error
	async def spam_error(self, ctx, error):
		await ctx.send(f"{error} The syntax is spam[number, message, is_session]")

	#Close Muxus and winston
	@cog_ext.cog_slash(name="stopWinston", guild_ids=server_ids, description="Stops Winston")
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