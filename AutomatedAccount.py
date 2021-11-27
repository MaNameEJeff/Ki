from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
from dotenv import load_dotenv
import time
import os

class AutomatedAccount():

    rate_limited = False

    #Initialize global variables and login to discord
    def __init__(self):
        global driver, text_field

        load_dotenv('.env')
        driver = webdriver.Firefox(executable_path=r'E:\Projects\Ki\geckodriver.exe')
        actions = ActionChains(driver)
        
        #Open discord in a new browser    
        driver.get("https://discord.com/channels/760880935557398608/792314109625499668")
        time.sleep(10)
        print ("Firefox Initialized")
    
        #Log onto discord
        text_field = driver.find_element_by_name('email')
        for character in os.getenv('EMAIL'):
            text_field.send_keys(character)
            time.sleep(0.3)
        text_field = driver.find_element_by_name('password')
        for character in os.getenv('PASSWORD'):
            text_field.send_keys(character)
            time.sleep(0.3)
        text_field.send_keys(Keys.RETURN)
        time.sleep(12)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
    
        #Look for message box
        time.sleep(3)
        text_field = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]')

    #Change to specific channel in discord
    def changeChannel(ctx, channel):
        global text_field

        #Open the quick change menu with the ctrl+k shortcut
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('k').key_up(Keys.CONTROL).perform()

        #Enter the name of the channel to move to and press enter
        time.sleep(0.5)
        text_field = driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div/div/div/input')
        text_field.send_keys(channel)
        time.sleep(1)
        text_field.send_keys(Keys.RETURN)
        time.sleep(3)

        #Look for message box
        text_field = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]')

    #Send specified message
    def say(ctx, text, self):

        global text_field
        actions = ActionChains(driver)

        #Try to send message or if rate limited stop and send error
        try:
            for character in text:
                text_field.send_keys(character)
                time.sleep(0.1)
            text_field.send_keys(Keys.RETURN)

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
    def close(ctx):
        driver.close()