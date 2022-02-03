from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
from dotenv import load_dotenv
import time
import os
import platform

class AutomatedAccount():

    #Initialize global variables and login to discord
    def __init__(self):

        load_dotenv('.env')

        self.rate_limited = False
        self.key_press_delay = 0.3
        self.general_path = "https://discord.com/channels/760880935557398608/"
        self.driver = webdriver.Firefox(executable_path=r'/opt/homebrew/bin/geckodriver')

        actions = ActionChains(self.driver)
        
        #Open discord in a new browser    
        self.driver.get(self.general_path + "792314109625499668")
        time.sleep(10)
        self.current_channel = 792314109625499668
        print ("Browser Initialized")
    
        #Log onto discord
        text_field = self.driver.find_element_by_name('email')
        for character in os.getenv('EMAIL'):
            text_field.send_keys(character)
            time.sleep(self.key_press_delay)
        text_field = self.driver.find_element_by_name('password')
        for character in os.getenv('PASSWORD'):
            text_field.send_keys(character)
            time.sleep(self.key_press_delay)
        text_field.send_keys(Keys.RETURN)

        #Wait until user confirms that login is done
        while True:
            test = input("Done?: ")
            if(test.upper() == "Y"):
                break

        #Press the escape key to close any popups that discord brings up
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
    
        #Look for message box
        time.sleep(3)
        self.text_field = self.driver.find_element_by_css_selector('.slateTextArea-27tjG0')

    #Change to specific channel in discord
    def changeChannel(self, channel_id):
        self.driver.get(self.general_path + str(channel_id))
        time.sleep(5)
        self.current_channel = int(channel_id)

        #Look for message box
        self.text_field = self.driver.find_element_by_css_selector('.slateTextArea-27tjG0')

    #Add reaction to a message
    def addReaction(self, message_id, reaction):

        #Look for the message sender avatar and click on it to reveal the add reaction menu for the message
        avatar = self.driver.find_element_by_css_selector(f"#chat-messages-{message_id} > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)")
        self.click(avatar)

        #Look for the add reaction button in the menu and click it to open the search bar
        add_reaction_button = self.driver.find_element_by_css_selector(f'#chat-messages-{message_id} > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > svg:nth-child(1)')
        self.click(add_reaction_button)

        #Search for the reaction and add it
        self.text_field = self.driver.find_element_by_css_selector(".input-1Rv96N")
        self.say(reaction)

    #Send specified message
    def say(self, text, clear_text_field=False):

        actions = ActionChains(self.driver)

        #Press CTRL+'a' or CMD+'a' and hit DEL to clear the text field
        if(clear_text_field):
            
            if("macOS" in platform.platform()):
                actions.key_down(Keys.COMMAND)
                actions.key_down('a')
                actions.key_up(Keys.COMMAND)
                actions.key_up('a')
            else:
                actions.key_down(Keys.CONTROL)
                actions.key_down('a')
                actions.key_up(Keys.CONTROL)
                actions.key_up('a')

            actions.send_keys(Keys.DELETE)
            actions.perform()

        #Try to send message or if rate limited stop and send error
        try:
            for character in text:
                self.text_field.send_keys(character)
                time.sleep(self.key_press_delay)
            self.text_field.send_keys(Keys.RETURN)

        except:
            time.sleep(3)
            actions.send_keys(Keys.RETURN)
            actions.perform()
            time.sleep(2)
            actions.send_keys(Keys.RETURN)
            actions.perform()
            time.sleep(1)
            actions.send_keys(Keys.RETURN)
            actions.perform()
            self.rate_limited = True
            return

    #Left click on an element on the screen
    def click(self, element):
        actions = ActionChains(self.driver)

        #Simulate mouse moment and click element
        actions.move_to_element(avatar)
        actions.perform()
        actions.click(on_element = avatar)
        actions.perform()
        time.sleep(2)

    #Close browser
    def close(self):
        self.driver.close()