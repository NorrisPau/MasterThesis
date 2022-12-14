from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set attributes
delay = 5
HOME_URL = "https://tinder.com/app/recs"

# Open Tinder using selenium
# Source: https://github.com/ifrankandrade/automation/blob/main/Tinder/en-tutorial.py
path = "/usr/local/bin/chromedriver"  # path of chrome driver
service = Service(executable_path=path)
web = 'https://tinder.com/'
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(service=service, options=options)
driver.get(web)  # Go to Tinder.com
driver.get(web)
time.sleep(3)

# Scraping
# 1. Click on Messages Button
matches_messages_path = '//button[@role="tab"]'  # Go to Tab with Button "Matches" and "Messages"
tabs = driver.find_elements(by="xpath", value=matches_messages_path)

time.sleep(10)

for tab in tabs:
    if tab.text == 'Messages':
        messages_button = tab
        driver.execute_script("arguments[0].click();", messages_button)
        # print("clicked on messages")

        # Conversation List
        xpath = '//div[@class="messageList"]'
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))  # wait for element

        # Go through each Conversation
        div = driver.find_element(By.XPATH, xpath)
        list_refs = div.find_elements(by="xpath", value='.//a')  # all conversations
        for index in range(len(list_refs)):  # for all matches conversations
            print("we have", len(list_refs), "tinder chats")
            print("____START: CHAT WITH MATCH", index, "____")
            driver.execute_script("arguments[0].click();", list_refs[index])  # open chat

            # All messages
            xpath_messages = '//div[starts-with(@class, "msgHelper")]'
            messages_helpers = driver.find_elements(By.XPATH, xpath_messages)

            #mMESSAGES RECEIVED
            # messages received:Content
            xpath_helpers_received = '//div[contains(@class, "msgHelper")]//div[contains(@class, "ds-text-chat-bubble-receive")]//span'
            helpers_received = driver.find_elements(By.XPATH, xpath_helpers_received)

            for message_received in helpers_received:
                print("received message is", message_received.text)
            # messages received:Time
            xpath_helpers_received_time = '//div[contains(@class, "Ta(start)")] //div[contains(@class, "msgHelper")]//time'
            helpers_received_time = driver.find_elements(By.XPATH, xpath_helpers_received_time)
            for time_message in helpers_received_time:
                print("time of received message is", time_message.get_attribute("datetime"))

            #MESSAGES SENT
            #Content
            xpath_helpers_sent = '//div[contains(@class, "msgHelper")]//div[contains(@class, "ds-text-chat-bubble-sent")]//span'
            helpers_sent = driver.find_elements(By.XPATH, xpath_helpers_sent)
            for message_sent in helpers_sent:
                print("sent message is", message_sent.text)
            #Time
            xpath_helpers_sent_time = '//div[contains(@class, "Ta(e)")] //div[contains(@class, "msgHelper")]//time'
            helpers_sent_time = driver.find_elements(By.XPATH, xpath_helpers_sent_time)
            for time_message_sent in helpers_sent_time:
                print("time of sent message is", time_message_sent.get_attribute("datetime"))

            time.sleep(5)
            print("END: CHAT WITH MATCH", index)
