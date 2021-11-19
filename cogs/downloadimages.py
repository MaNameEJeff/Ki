import discord
from discord.ext import commands
from discord_slash import cog_ext
import os

class downloadimages(commands.Cog):

	server_ids = [836276013830635590, 760880935557398608]

	def __init__(self, client):
		self.client = client

	@cog_ext.cog_slash(name="get_images", guild_ids=server_ids, description="Gets images from the number of messages specified in channel")
	async def get_images(self, ctx, channel_id, number_of_messages):

		#Check if message author is Jeff or not
		if(ctx.author.id != self.client.jeff_id):
			await ctx.send('Only MaNameEJeff can use this')
			return

		#Check respective channel
		if (int(channel_id) == self.client.incense_channel.id):
			image_channel = self.client.incense_channel
		elif (int(channel_id) == self.client.spawn_channel.id):
			image_channel = self.client.spawn_channel
		else:
			await ctx.send("Not a valid channel id")

		#Get images and store them as a list in pokemon
		await ctx.send('Downloading images...')
		pokemon = await image_channel.history(limit=int(number_of_messages)).flatten()
		j = 0
		for message in pokemon:
			if(message.author.id != self.client.poketwo_id):
				continue
			try:
				#Check if it is a spawn message
				if ((message.embeds[0].to_dict()['title'] == 'A wild pokémon has appeared!') or ('A new wild pokémon has appeared!' in message.embeds[0].to_dict()['title'])):
		
					#Get URL from image
					pokemon_URL = message.embeds[0].image.url

					#Download image to specified path
					img_args = "wget -O {0} {1}".format('E:/Projects/Ki/Images/' + str(j) + '.jpg', pokemon_URL)
					j = j+1
					os.system(img_args)

			except IndexError:
				continue

		await ctx.send("Done")

def setup(client):
	client.add_cog(downloadimages(client))