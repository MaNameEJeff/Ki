#Firebase

import pyrebase

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

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

	#Add another user
	def add_user(self, user_name):
		self.db.child("users").child(user_name).child("shiny").update({"pokemon": "None", "streak":0})
		self.db.child("users").child(user_name).child("list").update({"pokemon_list": "None"})
		self.db.child("users").child(user_name).child("quest").update({"quest": "None"})

def setup(client):
	client.add_cog(database(client))