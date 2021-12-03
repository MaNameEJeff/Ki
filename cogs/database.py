#Firebase

import pyrebase

import discord
from discord.ext import commands
from discord_slash import cog_ext

class database(commands.Cog):
	def __init__(self, client):

		self.client = client

		firebaseConfig = {
			"apiKey": "AIzaSyAc8yTPAFI6jYyjlZzq_CcP7BStiGuEg24",
			"authDomain": "discord-bot-ki.firebaseapp.com",
			"databaseURL": "https://discord-bot-ki-default-rtdb.firebaseio.com",
			"projectId": "discord-bot-ki",
			"storageBucket": "discord-bot-ki.appspot.com",
			"messagingSenderId": "908441491051",
			"appId": "1:908441491051:web:e49d4e1e910a1e72b0832e"
		}

		self.firebase = pyrebase.initialize_app(firebaseConfig)
		self.auth = self.firebase.auth()
		self.db = self.firebase.database()
		self.storage = self.firebase.storage()

	#Reinitialize the authenticated users
	def re_initialize_data_base(self):
		try:
			#Login the user
			winston = self.auth.sign_in_with_email_and_password("winstonemail@winston.com", "passwordwinston")
		except:
			winston = self.auth.create_user_with_email_and_password("winstonemail@winston.com", "passwordwinston")

	#Add another account that can be automated
	def add_automated_accounts(self, account_name, shiny):
		self.db.child("automated-accounts").child(account_name).child("shiny").update({"pokemon": "None"})
		self.db.child("automated-accounts").child(account_name).child("list").update({"pokemon_list": "None"})

def setup(client):
	client.add_cog(database(client))