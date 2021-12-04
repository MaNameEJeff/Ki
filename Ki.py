import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import menus

import os
import requests
import json
import time

from cogs import catching
from database import database
from UserListMenu import UserListMenu

client = commands.Bot(command_prefix = '.')
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)

#Runs when Bot is ready
@client.event
async def on_ready():

	#client.pokemon_in_game = ('Type: Null', 'Bulbasaur','Ivysaur','Venusaur','Charmander','Charmeleon','Charizard','Squirtle','Wartortle','Blastoise','Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill','Pidgey','Pidgeotto','Pidgeot','Rattata','Raticate','Spearow','Fearow','Ekans','Arbok','Pikachu','Raichu','Sandshrew','Sandslash','Nidoran♀️','Nidorina','Nidoqueen','Nidoran♂️','Nidorino','Nidoking','Clefairy','Clefable','Vulpix','Ninetales','Jigglypuff','Wigglytuff','Zubat','Golbat','Oddish','Gloom','Vileplume','Paras','Parasect','Venonat','Venomoth','Diglett','Dugtrio','Meowth','Persian','Psyduck','Golduck','Mankey','Primeape','Growlithe','Arcanine','Poliwag','Poliwhirl','Poliwrath','Abra','Kadabra','Alakazam','Machop','Machoke','Machamp','Bellsprout','Weepinbell','Victreebel','Tentacool','Tentacruel','Geodude','Graveler','Golem','Ponyta','Rapidash','Slowpoke','Slowbro','Magnemite','Magneton',"Farfetch'd",'Doduo','Dodrio','Seel','Dewgong','Grimer','Muk','Shellder','Cloyster','Gastly','Haunter','Gengar','Onix','Drowzee','Hypno','Krabby','Kingler','Voltorb','Electrode','Exeggcute','Exeggutor','Cubone','Marowak','Hitmonlee','Hitmonchan','Lickitung','Koffing','Weezing','Rhyhorn','Rhydon','Chansey','Tangela','Kangaskhan','Horsea','Seadra','Goldeen','Seaking','Staryu','Starmie','Mr. Mime','Scyther','Jynx','Electabuzz','Magmar','Pinsir','Tauros','Magikarp','Gyarados','Lapras','Ditto','Eevee','Vaporeon','Jolteon','Flareon','Porygon','Omanyte','Omastar','Kabuto','Kabutops','Aerodactyl','Snorlax','Articuno','Zapdos','Moltres','Dratini','Dragonair','Dragonite','Mewtwo','Mew','Chikorita','Bayleef','Meganium','Cyndaquil','Quilava','Typhlosion','Totodile','Croconaw','Feraligatr','Sentret','Furret','Hoothoot','Noctowl','Ledyba','Ledian','Spinarak','Ariados','Crobat','Chinchou','Lanturn','Pichu','Cleffa','Igglybuff','Togepi','Togetic','Natu','Xatu','Mareep','Flaaffy','Ampharos','Bellossom','Marill','Azumarill','Sudowoodo','Politoed','Hoppip','Skiploom','Jumpluff','Aipom','Sunkern','Sunflora','Yanma','Wooper','Quagsire','Espeon','Umbreon','Murkrow','Slowking','Misdreavus','Unown','Wobbuffet','Girafarig','Pineco','Forretress','Dunsparce','Gligar','Steelix','Snubbull','Granbull','Qwilfish','Scizor','Shuckle','Heracross','Sneasel','Teddiursa','Ursaring','Slugma','Magcargo','Swinub','Piloswine','Corsola','Remoraid','Octillery','Delibird','Mantine','Skarmory','Houndour','Houndoom','Kingdra','Phanpy','Donphan','Porygon2','Stantler','Smeargle','Tyrogue','Hitmontop','Smoochum','Elekid','Magby','Miltank','Blissey','Raikou','Entei','Suicune','Larvitar','Pupitar','Tyranitar','Lugia','Ho-Oh','Celebi','Treecko','Grovyle','Sceptile','Torchic','Combusken','Blaziken','Mudkip','Marshtomp','Swampert','Poochyena','Mightyena','Zigzagoon','Linoone','Wurmple','Silcoon','Beautifly','Cascoon','Dustox','Lotad','Lombre','Ludicolo','Seedot','Nuzleaf','Shiftry','Taillow','Swellow','Wingull','Pelipper','Ralts','Kirlia','Gardevoir','Surskit','Masquerain','Shroomish','Breloom','Slakoth','Vigoroth','Slaking','Nincada','Ninjask','Shedinja','Whismur','Loudred','Exploud','Makuhita','Hariyama','Azurill','Nosepass','Skitty','Delcatty','Sableye','Mawile','Aron','Lairon','Aggron','Meditite','Medicham','Electrike','Manectric','Plusle','Minun','Volbeat','Illumise','Roselia','Gulpin','Swalot','Carvanha','Sharpedo','Wailmer','Wailord','Numel','Camerupt','Torkoal','Spoink','Grumpig','Spinda','Trapinch','Vibrava','Flygon','Cacnea','Cacturne','Swablu','Altaria','Zangoose','Seviper','Lunatone','Solrock','Barboach','Whiscash','Corphish','Crawdaunt','Baltoy','Claydol','Lileep','Cradily','Anorith','Armaldo','Feebas','Milotic','Castform','Kecleon','Shuppet','Banette','Duskull','Dusclops','Tropius','Chimecho','Absol','Wynaut','Snorunt','Glalie','Spheal','Sealeo','Walrein','Clamperl','Huntail','Gorebyss','Relicanth','Luvdisc','Bagon','Shelgon','Salamence','Beldum','Metang','Metagross','Regirock','Regice','Registeel','Latias','Latios','Kyogre','Groudon','Rayquaza','Jirachi','Deoxys','Turtwig','Grotle','Torterra','Chimchar','Monferno','Infernape','Piplup','Prinplup','Empoleon','Starly','Staravia','Staraptor','Bidoof','Bibarel','Kricketot','Kricketune','Shinx','Luxio','Luxray','Budew','Roserade','Cranidos','Rampardos','Shieldon','Bastiodon','Burmy','Wormadam','Mothim','Combee','Vespiquen','Pachirisu','Buizel','Floatzel','Cherubi','Cherrim','Shellos','Gastrodon','Ambipom','Drifloon','Drifblim','Buneary','Lopunny','Mismagius','Honchkrow','Glameow','Purugly','Chingling','Stunky','Skuntank','Bronzor','Bronzong','Bonsly','Mime Jr.','Happiny','Chatot','Spiritomb','Gible','Gabite','Garchomp','Munchlax','Riolu','Lucario','Hippopotas','Hippowdon','Skorupi','Drapion','Croagunk','Toxicroak','Carnivine','Finneon','Lumineon','Mantyke','Snover','Abomasnow','Weavile','Magnezone','Lickilicky','Rhyperior','Tangrowth','Electivire','Magmortar','Togekiss','Yanmega','Leafeon','Glaceon','Gliscor','Mamoswine','Porygon-Z','Gallade','Probopass','Dusknoir','Froslass','Rotom','Uxie','Mesprit','Azelf','Dialga','Palkia','Heatran','Regigigas','Giratina','Cresselia','Phione','Manaphy','Darkrai','Shaymin','Arceus','Victini','Snivy','Servine','Serperior','Tepig','Pignite','Emboar','Oshawott','Dewott','Samurott','Patrat','Watchog','Lillipup','Herdier','Stoutland','Purrloin','Liepard','Pansage','Simisage','Pansear','Simisear','Panpour','Simipour','Munna','Musharna','Pidove','Tranquill','Unfezant','Blitzle','Zebstrika','Roggenrola','Boldore','Gigalith','Woobat','Swoobat','Drilbur','Excadrill','Audino','Timburr','Gurdurr','Conkeldurr','Tympole','Palpitoad','Seismitoad','Throh','Sawk','Sewaddle','Swadloon','Leavanny','Venipede','Whirlipede','Scolipede','Cottonee','Whimsicott','Petilil','Lilligant','Basculin','Sandile','Krokorok','Krookodile','Darumaka','Darmanitan','Maractus','Dwebble','Crustle','Scraggy','Scrafty','Sigilyph','Yamask','Cofagrigus','Tirtouga','Carracosta','Archen','Archeops','Trubbish','Garbodor','Zorua','Zoroark','Minccino','Cinccino','Gothita','Gothorita','Gothitelle','Solosis','Duosion','Reuniclus','Ducklett','Swanna','Vanillite','Vanillish','Vanilluxe','Deerling','Sawsbuck','Emolga','Karrablast','Escavalier','Foongus','Amoonguss','Frillish','Jellicent','Alomomola','Joltik','Galvantula','Ferroseed','Ferrothorn','Klink','Klang','Klinklang','Tynamo','Eelektrik','Eelektross','Elgyem','Beheeyem','Litwick','Lampent','Chandelure','Axew','Fraxure','Haxorus','Cubchoo','Beartic','Cryogonal','Shelmet','Accelgor','Stunfisk','Mienfoo','Mienshao','Druddigon','Golett','Golurk','Pawniard','Bisharp','Bouffalant','Rufflet','Braviary','Vullaby','Mandibuzz','Heatmor','Durant','Deino','Zweilous','Hydreigon','Larvesta','Volcarona','Cobalion','Terrakion','Virizion','Tornadus','Thundurus','Reshiram','Zekrom','Landorus','Kyurem','Keldeo','Meloetta','Genesect','Chespin','Quilladin','Chesnaught','Fennekin','Braixen','Delphox','Froakie','Frogadier','Greninja','Bunnelby','Diggersby','Fletchling','Fletchinder','Talonflame','Scatterbug','Spewpa','Vivillon','Litleo','Pyroar','Flabébé','Floette','Florges','Skiddo','Gogoat','Pancham','Pangoro','Furfrou','Espurr','Meowstic','Honedge','Doublade','Aegislash','Spritzee','Aromatisse','Swirlix','Slurpuff','Inkay','Malamar','Binacle','Barbaracle','Skrelp','Dragalge','Clauncher','Clawitzer','Helioptile','Heliolisk','Tyrunt','Tyrantrum','Amaura','Aurorus','Sylveon','Hawlucha','Dedenne','Carbink','Goomy','Sliggoo','Goodra','Klefki','Phantump','Trevenant','Pumpkaboo','Gourgeist','Bergmite','Avalugg','Noibat','Noivern','Xerneas','Yveltal','Zygarde','Diancie','Hoopa','Volcanion','Rowlet','Dartrix','Decidueye','Litten','Torracat','Incineroar','Popplio','Brionne','Primarina','Pikipek','Trumbeak','Toucannon','Yungoos','Gumshoos','Grubbin','Charjabug','Vikavolt','Crabrawler','Crabominable','Oricorio','Cutiefly','Ribombee','Rockruff','Lycanroc','Wishiwashi','Mareanie','Toxapex','Mudbray','Mudsdale','Dewpider','Araquanid','Fomantis','Lurantis','Morelull','Shiinotic','Salandit','Salazzle','Stufful','Bewear','Bounsweet','Steenee','Tsareena','Comfey','Oranguru','Passimian','Wimpod','Golisopod','Sandygast','Palossand','Pyukumuku','Type:Null','Silvally','Minior','Komala','Turtonator','Togedemaru','Mimikyu','Bruxish','Drampa','Dhelmise','Jangmo-o','Hakamo-o','Kommo-o','Tapu Koko','Tapu Lele','Tapu Bulu','Tapu Fini','Cosmog','Cosmoem','Solgaleo','Lunala','Nihilego','Buzzwole','Pheromosa','Xurkitree','Celesteela','Kartana','Guzzlord','Necrozma','Magearna','Marshadow','Poipole','Naganadel','Stakataka','Blacephalon','Zeraora','Meltan','Melmetal','Grookey','Thwackey','Rillaboom','Scorbunny','Raboot','Cinderace','Sobble','Drizzile','Inteleon','Skwovet','Greedent','Rookidee','Corvisquire','Corviknight','Blipbug','Dottler','Orbeetle','Nickit','Thievul','Gossifleur','Eldegoss','Wooloo','Dubwool','Chewtle','Drednaw','Yamper','Boltund','Rolycoly','Carkol','Coalossal','Applin','Flapple','Appletun','Silicobra','Sandaconda','Cramorant','Arrokuda','Barraskewda','Toxel','Toxtricity','Sizzlipede','Centiskorch','Clobbopus','Grapploct','Sinistea','Polteageist','Hatenna','Hattrem','Hatterene','Impidimp','Morgrem','Grimmsnarl','Obstagoon','Perrserker','Cursola',"Sirfetch'd",'Mr. Rime','Runerigus','Milcery','Alcremie','Falinks','Pincurchin','Snom','Frosmoth','Stonjourner','Eiscue','Indeedee','Morpeko','Cufant','Copperajah','Dracozolt','Arctozolt','Dracovish','Arctovish','Duraludon','Dreepy','Drakloak','Dragapult','Zacian','Zamazenta','Eternatus','Kubfu','Urshifu','Zarude','Regieleki','Regidrago','Glastrier','Spectrier')
	
	#Changed tuple to an organized dictionary, corresponding changes made in shinyhunt.py
	client.pokemon_in_game = {
		3: ['Mew', 'Muk'],
		4: ['Abra', 'Aron', 'Axew', 'Jynx', 'Natu', 'Onix', 'Sawk', 'Seel', 'Snom', 'Uxie', 'Xatu'], 
		5: ['Absol', 'Aipom', 'Arbok', 'Azelf', 'Bagon', 'Budew', 'Burmy', 'Deino', 'Ditto', 'Doduo', 'Eevee', 'Ekans', 'Entei', 'Gible', 'Gloom', 'Golem', 'Goomy', 'Ho-Oh', 'Hoopa', 'Hypno', 'Inkay', 'Klang', 'Klink', 'Kubfu', 'Lotad', 'Lugia', 'Luxio', 'Magby', 'Minun', 'Munna', 'Numel', 'Paras', 'Pichu', 'Ralts', 'Riolu', 'Rotom', 'Shinx', 'Snivy', 'Tepig', 'Throh', 'Toxel', 'Unown', 'Yanma', 'Zorua', 'Zubat'], 
		6: ['Aggron', 'Amaura', 'Applin', 'Arceus', 'Archen', 'Audino', 'Baltoy', 'Beldum', 'Bewear', 'Bidoof', 'Bonsly', 'Buizel', 'Cacnea', 'Carkol', 'Celebi', 'Chatot', 'Cleffa', 'Combee', 'Comfey', 'Cosmog', 'Crobat', 'Cubone', 'Cufant', 'Deoxys', 'Dewott', 'Dialga', 'Dodrio', 'Drampa', 'Dreepy', 'Durant', 'Dustox', 'Eiscue', 'Elekid', 'Elgyem', 'Emboar', 'Emolga', 'Espeon', 'Espurr', 'Fearow', 'Feebas', 'Flygon', 'Furret', 'Gabite', 'Gastly', 'Gengar', 'Glalie', 'Gligar', 'Gogoat', 'Golbat', 'Golett', 'Golurk', 'Goodra', 'Grimer', 'Grotle', 'Gulpin', 'Hoppip', 'Horsea', 'Joltik', 'Kabuto', 'Kakuna', 'Keldeo', 'Kirlia', 'Klefki', 'Komala', 'Krabby', 'Kyogre', 'Kyurem', 'Lairon', 'Lapras', 'Latias', 'Latios', 'Ledian', 'Ledyba', 'Lileep', 'Litleo', 'Litten', 'Lombre', 'Lunala', 'Luxray', 'Machop', 'Magmar', 'Mankey', 'Mareep', 'Marill', 'Mawile', 'Meltan', 'Meowth', 'Metang', 'Mewtwo', 'Minior', 'Mothim', 'Mudkip', 'Nickit', 'Noibat', 'Oddish', 'Palkia', 'Patrat', 'Phanpy', 'Phione', 'Pidgey', 'Pidove', 'Pineco', 'Pinsir', 'Piplup', 'Plusle', 'Ponyta', 'Pyroar', 'Raboot', 'Raichu', 'Raikou', 'Regice', 'Rhydon', 'Rowlet', 'Scizor', 'Seadra', 'Sealeo', 'Seedot', 'Skiddo', 'Skitty', 'Skrelp', 'Slugma', 'Snover', 'Sobble', 'Spewpa', 'Spheal', 'Spinda', 'Spoink', 'Starly', 'Staryu', 'Stunky', 'Swablu', 'Swalot', 'Swanna', 'Swinub', 'Tauros', 'Togepi', 'Tynamo', 'Tyrunt', 'Vulpix', 'Weedle', 'Wimpod', 'Woobat', 'Wooloo', 'Wooper', 'Wynaut', 'Yamask', 'Yamper', 'Zacian', 'Zapdos', 'Zarude', 'Zekrom'], 
		7: ['Altaria', 'Ambipom', 'Anorith', 'Ariados', 'Armaldo', 'Aurorus', 'Avalugg', 'Azurill', 'Banette', 'Bayleef', 'Beartic', 'Bibarel', 'Binacle', 'Bisharp', 'Blipbug', 'Blissey', 'Blitzle', 'Boldore', 'Boltund', 'Braixen', 'Breloom', 'Brionne', 'Bronzor', 'Bruxish', 'Buneary', 'Carbink', 'Cascoon', 'Chansey', 'Cherrim', 'Cherubi', 'Chespin', 'Chewtle', 'Claydol', 'Corsola', 'Cosmoem', 'Cradily', 'Crustle', 'Cubchoo', 'Cursola', 'Darkrai', 'Dartrix', 'Dedenne', 'Delphox', 'Dewgong', 'Diancie', 'Diglett', 'Donphan', 'Dottler', 'Drapion', 'Dratini', 'Drednaw', 'Drilbur', 'Drowzee', 'Dubwool', 'Dugtrio', 'Duosion', 'Duskull', 'Dwebble', 'Exploud', 'Falinks', 'Finneon', 'Flaaffy', 'Flabebe', 'Flapple', 'Flareon', 'Floette', 'Florges', 'Foongus', 'Fraxure', 'Froakie', 'Furfrou', 'Gallade', 'Geodude', 'Glaceon', 'Glameow', 'Gliscor', 'Goldeen', 'Golduck', 'Gothita', 'Grookey', 'Groudon', 'Grovyle', 'Grubbin', 'Grumpig', 'Gurdurr', 'Happiny', 'Hatenna', 'Hattrem', 'Haunter', 'Haxorus', 'Heatmor', 'Heatran', 'Herdier', 'Honedge', 'Huntail', 'Ivysaur', 'Jirachi', 'Jolteon', 'Kadabra', 'Kartana', 'Kecleon', 'Kingdra', 'Kingler', 'Koffing', 'Kommo-o', 'Lampent', 'Lanturn', 'Leafeon', 'Liepard', 'Linoone', 'Litwick', 'Lopunny', 'Loudred', 'Lucario', 'Luvdisc', 'Machamp', 'Machoke', 'Malamar', 'Manaphy', 'Mantine', 'Mantyke', 'Marowak', 'Mesprit', 'Metapod', 'Mienfoo', 'Milcery', 'Milotic', 'Miltank', 'MimeJr.', 'Mimikyu', 'Moltres', 'Morgrem', 'Morpeko', 'Mr.Mime', 'Mr.Rime', 'Mudbray', 'Murkrow', 'Nidoran', 'Nincada', 'Ninjask', 'Noctowl', 'Noivern', 'Nuzleaf', 'Omanyte', 'Omastar', 'Pancham', 'Pangoro', 'Panpour', 'Pansage', 'Pansear', 'Persian', 'Petilil', 'Pidgeot', 'Pignite', 'Pikachu', 'Pikipek', 'Poipole', 'Poliwag', 'Popplio', 'Porygon', 'Psyduck', 'Pupitar', 'Purugly', 'Quilava', 'Rattata', 'Rhyhorn', 'Roselia', 'Rufflet', 'Sableye', 'Sandile', 'Scrafty', 'Scraggy', 'Scyther', 'Seaking', 'Sentret', 'Servine', 'Seviper', 'Shaymin', 'Shelgon', 'Shellos', 'Shelmet', 'Shiftry', 'Shuckle', 'Shuppet', 'Silcoon', 'Skorupi', 'Skwovet', 'Slaking', 'Slakoth', 'Sliggoo', 'Slowbro', 'Sneasel', 'Snorlax', 'Snorunt', 'Solosis', 'Solrock', 'Spearow', 'Starmie', 'Steelix', 'Steenee', 'Stufful', 'Suicune', 'Sunkern', 'Surskit', 'Swellow', 'Swirlix', 'Swoobat', 'Sylveon', 'Taillow', 'Tangela', 'Thievul', 'Timburr', 'Togetic', 'Torchic', 'Torkoal', 'Toxapex', 'Treecko', 'Tropius', 'Turtwig', 'Tympole', 'Tyrogue', 'Umbreon', 'Urshifu', 'Venonat', 'Vibrava', 'Victini', 'Volbeat', 'Voltorb', 'Vullaby', 'Wailmer', 'Wailord', 'Walrein', 'Watchog', 'Weavile', 'Weezing', 'Whismur', 'Wingull', 'Wurmple', 'Xerneas', 'Yanmega', 'Yungoos', 'Yveltal', 'Zeraora', 'Zoroark', 'Zygarde', 'Calyrex'], 
		8: ['Accelgor', 'Alakazam', 'Alcremie', 'Ampharos', 'Appletun', 'Arcanine', 'Archeops', 'Arrokuda', 'Articuno', 'Barboach', 'Basculin', 'Beedrill', 'Beheeyem', 'Bergmite', 'Blaziken', 'Braviary', 'Bronzong', 'Bunnelby', 'Buzzwole', 'Cacturne', 'Camerupt', 'Carvanha', 'Castform', 'Caterpie', 'Chimchar', 'Chimecho', 'Chinchou', 'Cinccino', 'Clamperl', 'Clefable', 'Clefairy', 'Cloyster', 'Cobalion', 'Corphish', 'Cottonee', 'Cranidos', 'Croagunk', 'Croconaw', 'Cutiefly', 'Darumaka', 'Deerling', 'Delcatty', 'Delibird', 'Dewpider', 'Dhelmise', 'Doublade', 'Dragalge', 'Drakloak', 'Drifblim', 'Drifloon', 'Drizzile', 'Ducklett', 'Dusclops', 'Dusknoir', 'Eldegoss', 'Empoleon', 'Fennekin', 'Floatzel', 'Fomantis', 'Frillish', 'Froslass', 'Frosmoth', 'Garbodor', 'Garchomp', 'Genesect', 'Gigalith', 'Giratina', 'Gorebyss', 'Granbull', 'Graveler', 'Greedent', 'Greninja', 'Gumshoos', 'Guzzlord', 'Gyarados', 'Hakamo-o', 'Hariyama', 'Hawlucha', 'Hoothoot', 'Houndoom', 'Houndour', 'Illumise', 'Impidimp', 'Indeedee', 'Inteleon', 'Jangmo-o', 'Jumpluff', 'Kabutops', 'Krokorok', 'Landorus', 'Larvesta', 'Larvitar', 'Leavanny', 'Lillipup', 'Ludicolo', 'Lumineon', 'Lunatone', 'Lurantis', 'Lycanroc', 'Magcargo', 'Magearna', 'Magikarp', 'Magneton', 'Makuhita', 'Maractus', 'Mareanie', 'Medicham', 'Meditite', 'Meganium', 'Melmetal', 'Meloetta', 'Meowstic', 'Mienshao', 'Minccino', 'Monferno', 'Morelull', 'Mudsdale', 'Munchlax', 'Musharna', 'Necrozma', 'Nidoking', 'Nidorina', 'Nidorino', 'Nihilego', 'Nosepass', 'Oranguru', 'Orbeetle', 'Oricorio', 'Oshawott', 'Parasect', 'Pawniard', 'Pelipper', 'Phantump', 'Politoed', 'Porygon2', 'Primeape', 'Prinplup', 'Purrloin', 'Quagsire', 'Qwilfish', 'Rapidash', 'Raticate', 'Rayquaza', 'Regirock', 'Remoraid', 'Reshiram', 'Ribombee', 'Rockruff', 'Rolycoly', 'Rookidee', 'Roserade', 'Salandit', 'Salazzle', 'Samurott', 'Sawsbuck', 'Sceptile', 'Sewaddle', 'Sharpedo', 'Shedinja', 'Shellder', 'Shieldon', 'Sigilyph', 'Silvally', 'Simipour', 'Simisage', 'Simisear', 'Sinistea', 'Skarmory', 'Skiploom', 'Skuntank', 'Slowking', 'Slowpoke', 'Slurpuff', 'Smeargle', 'Smoochum', 'Snubbull', 'Solgaleo', 'Spinarak', 'Spritzee', 'Squirtle', 'Stantler', 'Staravia', 'Stunfisk', 'Sunflora', 'Swadloon', 'Swampert', 'Thwackey', 'Tirtouga', 'Togekiss', 'Tornadus', 'Torracat', 'Torterra', 'Totodile', 'Trapinch', 'Trubbish', 'Trumbeak', 'Tsareena', 'Unfezant', 'Ursaring', 'Vaporeon', 'Venipede', 'Venomoth', 'Venusaur', 'Vigoroth', 'Vikavolt', 'Virizion', 'Vivillon', 'Whiscash', 'Wormadam', 'Zangoose', 'Zweilous'], 
		9: ['Abomasnow', 'Aegislash', 'Alomomola', 'Amoonguss', 'Araquanid', 'Arctovish', 'Arctozolt', 'Azumarill', 'Bastiodon', 'Beautifly', 'Bellossom', 'Blastoise', 'Bounsweet', 'Bulbasaur', 'Carnivine', 'Charizard', 'Charjabug', 'Chikorita', 'Chingling', 'Cinderace', 'Clauncher', 'Clawitzer', 'Clobbopus', 'Coalossal', 'Combusken', 'Cramorant', 'Crawdaunt', 'Cresselia', 'Cryogonal', 'Cyndaquil', 'Decidueye', 'Diggersby', 'Dracovish', 'Dracozolt', 'Dragapult', 'Dragonair', 'Dragonite', 'Druddigon', 'Dunsparce', 'Duraludon', 'Eelektrik', 'Electrike', 'Electrode', 'Eternatus', 'Excadrill', 'Exeggcute', 'Exeggutor', 'Ferroseed', 'Frogadier', 'Gardevoir', 'Gastrodon', 'Girafarig', 'Glastrier', 'Golisopod', 'Gothorita', 'Gourgeist', 'Grapploct', 'Growlithe', 'Hatterene', 'Heliolisk', 'Heracross', 'Hippowdon', 'Hitmonlee', 'Hitmontop', 'Honchkrow', 'Hydreigon', 'Igglybuff', 'Infernape', 'Jellicent', 'Klinklang', 'Kricketot', 'Lickitung', 'Lilligant', 'Magmortar', 'Magnemite', 'Magnezone', 'Mamoswine', 'Mandibuzz', 'Manectric', 'Marshadow', 'Marshtomp', 'Metagross', 'Mightyena', 'Mismagius', 'Naganadel', 'Nidoqueen', 'Ninetales', 'Obstagoon', 'Octillery', 'Pachirisu', 'Palossand', 'Palpitoad', 'Passimian', 'Pheromosa', 'Pidgeotto', 'Piloswine', 'Poliwhirl', 'Poliwrath', 'Poochyena', 'Porygon-Z', 'Primarina', 'Probopass', 'Pumpkaboo', 'Pyukumuku', 'Quilladin', 'Rampardos', 'Regidrago', 'Regieleki', 'Regigigas', 'Registeel', 'Relicanth', 'Reuniclus', 'Rhyperior', 'Rillaboom', 'Runerigus', 'Salamence', 'Sandshrew', 'Sandslash', 'Sandygast', 'Scolipede', 'Scorbunny', 'Serperior', 'Shiinotic', 'Shroomish', 'Silicobra', 'Spectrier', 'Spiritomb', 'Stakataka', 'Staraptor', 'Stoutland', 'Sudowoodo', 'Tangrowth', 'Tapu Bulu', 'Tapu Fini', 'Tapu Koko', 'Tapu Lele', 'Teddiursa', 'Tentacool', 'Terrakion', 'Thundurus', 'Toucannon', 'Toxicroak', 'Tranquill', 'Trevenant', 'Tyranitar', 'Tyrantrum', 'Vanillish', 'Vanillite', 'Vanilluxe', 'Vespiquen', 'Vileplume', 'Volcanion', 'Volcarona', 'Wartortle', 'Wobbuffet', 'Xurkitree', 'Zamazenta', 'Zebstrika', 'Zigzagoon'], 
		10: ['Aerodactyl', 'Aromatisse', 'Barbaracle', 'Bellsprout', 'Bouffalant', 'Butterfree', 'Carracosta', 'Celesteela', 'Chandelure', 'Charmander', 'Charmeleon', 'Chesnaught', 'Cofagrigus', 'Conkeldurr', 'Copperajah', 'Crabrawler', 'Darmanitan', 'Eelektross', 'Electabuzz', 'Electivire', 'Escavalier', "Farfetch'd", 'Feraligatr', 'Ferrothorn', 'Fletchling', 'Forretress', 'Galvantula', 'Gossifleur', 'Gothitelle', 'Grimmsnarl', 'Helioptile', 'Hippopotas', 'Hitmonchan', 'Incineroar', 'Jigglypuff', 'Kangaskhan', 'Karrablast', 'Kricketune', 'Krookodile', 'Lickilicky', 'Masquerain', 'Misdreavus', 'Perrserker', 'Pincurchin', 'Roggenrola', 'Sandaconda', 'Scatterbug', 'Seismitoad', "Sirfetch'd", 'Sizzlipede', 'Talonflame', 'Tentacruel', 'Togedemaru', 'Toxtricity', 'Turtonator', 'Type: Null', 'Typhlosion', 'Victreebel', 'Weepinbell', 'Whimsicott', 'Whirlipede', 'Wigglytuff', 'Wishiwashi'], 
		11: ['Barraskewda', 'Blacephalon', 'Centiskorch', 'Corviknight', 'Corvisquire', 'Fletchinder', 'Polteageist', 'Stonjourner'], 
		12: ['Crabominable']
	}

	#Initialize Discord channels
	for guild in client.guilds:
		if(guild.name == "Winston's server"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 881875552028483594):
					client.pokemon_names_channel = text_channel
				elif(text_channel.id == 882583920963625010):
					client.spam_channel = text_channel
				elif(text_channel.id == 882872744323203072):
					client.command_channel = text_channel

		elif(guild.name == "The Bois"):
			for text_channel in guild.text_channels:
				if(text_channel.id == 792314109625499668):
					client.spawn_channel = text_channel
				elif(text_channel.id == 851101277920559154):
					client.incense_channel = text_channel
				elif(text_channel.id == 789868961071628348):
					client.bot_channel = text_channel

	#Initialize ids
	client.moto_id = 730020582393118730
	client.ganther_id = 730028657581490176
	client.jeff_id = 730023436939952139
	client.spex_id = 729997258656972820
	client.poketwo_id = 716390085896962058

	client.winston_status = False

	#Initialize objects
	client.catch = catching.catching(client)
	client.data_base = database()
	client.user_list_menu = UserListMenu()

	print('ready')

#Runs whenever a message is posted on Discord
@client.event
async def on_message(message):

	#Check if Muxus says accounts are being rate limited
	if((message.author.id == 882580519542468639) and (message.channel.id == client.command_channel.id) and (message.content == 'Rate Limited')):
		await client.spawn_channel.send("Accounts are being rate limited right now... Try that again after a few seconds")
		await client.command_channel.purge(limit=1) #Remove the rate limited message afterwards
		return

	#Check to see if messsage if from poketwo in the spawn channel
	if((message.author.id == client.poketwo_id) and (message.channel.id == client.spawn_channel.id)):

		if(client.winston_status == False):
			return

		try:

			#Get the message from poketwo
			pokemon_spawn_message = (await message.channel.fetch_message(message.id)).embeds[0]

			#Check if it is a spawn message
			if ('wild pokémon has appeared!' in pokemon_spawn_message.to_dict().get('title')):
								
				#Get URL and name of pokemon
				poke = await client.catch.who_catches()
				pokemon_URL = pokemon_spawn_message.image.url
				path = f"E:/Projects/Ki/Images/{poke}"

				#Ask Muxus to download it to directory
				await client.spawn_channel.send(f"Downloading image to {path}")
				await client.command_channel.send(f"Download {pokemon_URL} {path}")

		except IndexError:
			return

	#Runs on_message alongside other commands
	await client.process_commands(message)

#Send numbers from start till end
@slash.slash(
	name="numbers",
	description="Sends numbers from start till end",
	guild_ids=[760880935557398608],
	options=[
		create_option(
			name="start",
			description="Starting number",
			option_type=4,
			required=True
		),
		create_option(
			name="end",
			description="Ending number",
			option_type=4,
			required=True
		)
	]
)

async def numbers(ctx:SlashContext, start, end):
	s = ""

	if(end < start):
		for i in range(int(start), int(end)-1, -1):
			s += str(i) + " "
	else:
		for i in range(int(start), int(end)+1):
			s += str(i) + " "

	await ctx.send(s)

#Load all cogs in cogs folder
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

#Run the bot
client.run(os.environ['TOKEN'])