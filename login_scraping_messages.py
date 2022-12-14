from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Set attributes
delay = 5
HOME_URL = "https://tinder.com/app/recs"

#Open Tinder using selenium
#Source: https://github.com/ifrankandrade/automation/blob/main/Tinder/en-tutorial.py
path = "/usr/local/bin/chromedriver" #path of chrome driver
service = Service(executable_path=path)
web = 'https://tinder.com/'
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(service=service, options=options)
driver.get(web) #Go to Tinder.com
driver.get(web)
time.sleep(3)

#Scraping
#1. Click on Messages Button
matches_messages_path = '//button[@role="tab"]' #Go to Tab with Button "Matches" and "Messages"
tabs = driver.find_elements(by="xpath", value=matches_messages_path)

for tab in tabs:
    if tab.text == 'Messages':
        messages_button = tab
        driver.execute_script("arguments[0].click();", messages_button)
        print("clicked on messages")

        #Messages List
        xpath = '//div[@class="messageList"]'
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath))) #wait until element appears

        div = driver.find_element(By.XPATH, xpath)
        list_refs = div.find_elements(by="xpath", value='.//a') #all conversations
        for index in range(len(list_refs)):
            print("we have", len(list_refs), "tinder chats")
            driver.execute_script("arguments[0].click();", list_refs[index]) #open each chat
            time.sleep(5)
            print("chat", index, "was clicked")






