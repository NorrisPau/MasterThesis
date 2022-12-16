from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import uuid  # to make match id
import pandas as pd

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
time.sleep(3)
wait = WebDriverWait(driver, 10)

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
        xpath_messageList = '//div[@class="messageList"]'

        # Go through each Conversation
        div = wait.until(lambda driver: driver.find_element(By.XPATH, xpath_messageList))
        #div = driver.find_element(By.XPATH, xpath)

        list_refs = div.find_elements(by="xpath", value='.//a')  # all conversations
        match_id_lst = []
        message_count_lst = []
        print("we have chats with", len(list_refs), "matches")

        for index in range(len(list_refs)):  # for all matches
            match_id_lst.append(uuid.uuid4())
            print("match_id_lst is", match_id_lst)

            print("____START: CHAT WITH MATCH", index, "ID:   ", match_id_lst[index], "____")

            driver.execute_script("arguments[0].click();", list_refs[index])  # open chat
            time.sleep(3)  # wait for messages to appear

            # All messages
            xpath_messages = '//div[starts-with(@class, "msgHelper")]'
            message_helpers = wait.until(lambda driver: driver.find_elements(By.XPATH, xpath_messages))

            # MESSAGES RECEIVED
            xpath_received_msgHelper = '//div[contains(@class, "Ta(start)")]//div[contains(@class, "msgHelper")]'
            xpath_helpers_received = xpath_received_msgHelper + '//div[contains(@class, "ds-text-chat-bubble-receive")]//span'  # content
            xpath_helpers_received_time = xpath_received_msgHelper + '//time'  # time
            helpers_received = wait.until(lambda driver: driver.find_elements(By.XPATH, xpath_helpers_received))
            # MESSAGES SENT
            xpath_sent_helper = '//div[contains(@class, "Ta(e)")] //div[contains(@class, "msgHelper")]'
            xpath_helpers_sent = xpath_sent_helper + '//span'  # //div[contains(@class, "ds-text-chat-bubble-sent")]
            xpath_helpers_sent_time = xpath_sent_helper + '//time'
            helpers_sent = driver.find_elements(By.XPATH, xpath_helpers_sent)

            print("This Chat has", len(helpers_received), "messages received, and", len(helpers_sent), "messages sent")
            message_count_lst.append(int(len(helpers_received)+len(helpers_sent)))

            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath_received_msgHelper)))  # wait for element

            received_messages_lst = []
            received_messages_time_lst = []

            for message_received in range(len(helpers_received)):
                print("received message is", helpers_received[message_received].text)
                received_messages_lst.append(helpers_received[message_received].text)
            # messages received:Time
            helpers_received_time = driver.find_elements(By.XPATH, xpath_helpers_received_time)
            for time_message in helpers_received_time:
                print("time of received message is", time_message.get_attribute("datetime"))
                received_messages_time_lst.append(time_message.get_attribute("datetime"))

            # MESSAGES SENT
            sent_messages_lst = []
            sent_messages_time_lst = []
            # Content
            for message_sent in range(len(helpers_sent)):
                print("sent message is", helpers_sent[message_sent].text)
                sent_messages_lst.append(helpers_sent[message_sent].text)

            # Time
            helpers_sent_time = driver.find_elements(By.XPATH, xpath_helpers_sent_time)
            for time_message_sent in helpers_sent_time:
                print("time of sent message is", time_message_sent.get_attribute("datetime"))
                sent_messages_time_lst.append(time_message_sent.get_attribute("datetime"))


            time.sleep(10)
            print("END: CHAT WITH MATCH", index)
            #TODO: Handle Time Error which appears after 26 conversations
