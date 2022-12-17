from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

token_RE = "'TinderWeb\/APIToken': '(?P<token>([\w-])+)'"
max_retries = 10

driver = webdriver.Remote(
   command_executor='http://localhost:4444/wd/hub',
desired_capabilities={'browserName': "firefox", 'javascriptEnabled': True})
driver.get("http://www.tinder.com")
#print(driver.get_cookies())

while True:
    local_storage = str(driver.execute_script("return window.localStorage;"))
    if re.match(token_RE, local_storage):
        fb_token = re.search(token_RE, local_storage).group("token")
        print(f'FOUND TOKEN {fb_token} in {local_storage}')
        driver.quit()
        break
    elif max_retries < 1:
        driver.quit()
        break
    else:
        time.sleep(10)
        print(f'DEBUG \n PAGE: {driver.current_url} \n LOCAL STORAGE: {local_storage}') 

