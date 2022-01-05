from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
from dotenv import load_dotenv
import time
import os

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
        print(type(self.current_channel))
        print ("Firefox Initialized")
    
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

        while True:
            test = input("Done?: ")
            if(test.upper() == "Y"):
                break

        actions.send_keys(Keys.ESCAPE)
        actions.perform()
    
        #Look for message box
        time.sleep(3)
        self.text_field = self.driver.find_element_by_css_selector('.slateTextArea-1Mkdgw')

    #Change to specific channel in discord
    def changeChannel(self, channel_id):
        self.driver.get(self.general_path + str(channel_id))
        time.sleep(5)
        self.current_channel = int(channel_id)

        #Look for message box
        self.text_field = self.driver.find_element_by_css_selector('.slateTextArea-1Mkdgw')

    #Send specified message
    def say(self, text):

        actions = ActionChains(self.driver)

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

    #Close browser
    def close(self):
        self.driver.close()