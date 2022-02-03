#Firebase initialization
import pyrebase

class database():
	def __init__(self):

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
		