#Paginated Embeds of user list

from discord.ext import menus
from discord import Embed

class UserListMenu(menus.Menu):

    pages=[]
    current_page_number = 0

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.pages[0])

    #If back arrow is clicked edit message to display previous embed
    @menus.button('◀️')
    async def next_page(self, payload):
        try:
            await self.message.edit(embed=self.pages[self.current_page_number - 1])
            self.current_page_number -= 1
        except IndexError:
            return

    #If forward arrow is clicked edit message to display next embed
    @menus.button('▶️')
    async def previous_page(self, payload):
        try:
            await self.message.edit(embed=self.pages[self.current_page_number + 1])
            self.current_page_number += 1
        except IndexError:
            return

    #Set the embed data
    def set_data(self, data):
        self.pages.extend(data)