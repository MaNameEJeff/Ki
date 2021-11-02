import discord
from discord.ext import commands

class winston(commands.Cog):

	def __init__(self, client):
		self.client = client

	#Spam
	@commands.command()
	async def spam(self, ctx, number=5, text = "spam", is_session=False):
	
		if(self.client.var_winston_status == False):
			await self.client.checkWinstonStatus()
	
		if((self.client.var_winston_status) and (is_session == False)):
			await ctx.send(f'Spamming {number} messages...')
			await self.client.var_spam_channel.send(str(number) + " " + text + " " + str(is_session))
	
		elif((self.client.var_winston_status) and (is_session)):
			await ctx.send("Starting a session")
			await self.client.var_spam_channel.send(str(number) + " " + text + " " + str(is_session))
	
		else:
			await ctx.send('Sorry Winston seems to be offline...')
	
	#Stop Winston spamming
	@commands.command()
	async def stopSpam(self, ctx):
		await ctx.send("Stopping session")
		await self.client.var_command_channel.send("Stop Spam")
	
	#Handle invalid arguments
	@spam.error
	async def spam_error(self, ctx, error):
		await ctx.send(f"{error} The syntax is spam[number, message, is_session]")

	#Close Muxus
	@commands.command()
	async def stopWinston(self, ctx):
	
		#Check winston status and if he's offline exit
		if(self.client.var_winston_status == False):
			await self.client.checkWinstonStatus()
	
		if(self.client.var_winston_status == False):
			await ctx.send('Winston is already offline')
			return
	
		#Send prompt, clear messages in Winston's server and exit
		await ctx.send('Closing Winston')
		await self.client.var_command_channel.send('Leave')
		await self.client.var_command_channel.purge(limit=1000)
		await self.client.var_output_channel.purge(limit=1000)
		await self.client.var_spam_channel.purge(limit=1000)
		self.client.var_winston_status = False
		await ctx.send('Winston is now offline')

		print(self.client.var_winston_status)

def setup(client):
	client.add_cog(winston(client))