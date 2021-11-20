import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import os

class downloadimages(commands.Cog):

	server_ids = [760880935557398608]

	def __init__(self, client):
		self.client = client

	@cog_ext.cog_slash(	name="get_images",
						guild_ids=server_ids,
						description="Gets images from the number of messages specified in channel",
						options=[
							create_option(
								name="channel",
								description="The channel to download images from",
								option_type=7,
								required=True
							),
							create_option(
								name="number_of_messages",
								description="The number of messages to check",
								option_type=4,
								required=True
							)
						]
					  )
	
	async def get_images(self, ctx, channel, number_of_messages):

		#Check if message author is Jeff or not
		if(ctx.author.id != self.client.jeff_id):
			await ctx.send('Only MaNameEJeff can use this')
			return

		#Get images and store them as a list in pokemon
		await ctx.send('Downloading images...')
		pokemon = await channel.history(limit=int(number_of_messages)).flatten()
		j = 0
		for message in pokemon:
			if(message.author.id != self.client.poketwo_id):
				continue
			try:
				#Check if it is a spawn message
				if ('wild pokémon has appeared!' in message.embeds[0].to_dict().get('title')):
		
					#Get URL from image
					pokemon_URL = message.embeds[0].image.url

					if("Images" not in os.listdir("./")):
						os.system('mkdir Images')

					#Download image to specified path
					img_args = "wget -O {0} {1}".format('E:/Projects/Ki/Images/' + str(j) + '.jpg', pokemon_URL)
					j += 1
					os.system(img_args)

			except IndexError:
				continue

		await ctx.send("Done")

def setup(client):
	client.add_cog(downloadimages(client))