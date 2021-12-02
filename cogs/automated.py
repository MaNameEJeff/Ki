#Cog with all commands related to automated accounts

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

class automated(commands.Cog):

	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client
	
	#Updates account status
	@cog_ext.cog_slash( name="check_account_status",
						guild_ids=server_ids,
						description="Updates status of accounts that can be automated"
					  )

	async def check_account_status(self, ctx):

		#Check the command channel in Winston's server to see if Muxus says accounts are online
		status = (await self.client.command_channel.history(limit=1).flatten())[0].content
		if (status == "online"):
			await ctx.send("Accounts are online")
			self.client.winston_status = True
		else:
			await ctx.send("Accounts are offline")

	#Spam
	@cog_ext.cog_slash(	name="spam",
						guild_ids=server_ids,
						description="Spam",
						options=[
							create_option(
								name="spam_tasks",
								description="Manage Accounts",
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
			await ctx.send('Sorry no account is online...')
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
	
		#Stop spamming
		elif(spam_tasks == "Stop"):
			await ctx.send("Stopping session")
			await self.client.command_channel.send("Stop Spam")
		
	#Close Muxus and all accounts
	@cog_ext.cog_slash(	name="stopAllAccounts",
						guild_ids=server_ids,
						description="Stops all running accounts"
					  )

	async def stopAllAccounts(self, ctx):
	
		if(self.client.winston_status == False):
			await ctx.send('Accounts are already offline')
			return
	
		#Send prompt, clear messages in Winston's server and exit
		await ctx.send('Closing...')
		await self.client.command_channel.purge(limit=1000)
		await self.client.pokemon_names_channel.purge(limit=1000)
		await self.client.spam_channel.purge(limit=1000)
		await self.client.command_channel.send('Leave')
		self.client.winston_status = False
		await ctx.send('All accounts are now offline')

def setup(client):
	client.add_cog(automated(client))