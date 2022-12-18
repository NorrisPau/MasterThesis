from selenium import webdriver
from selenium_stealth import stealth
import time
import re
import requests
import uuid

from tinder_api import get_messages

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
token_RE = "'TinderWeb\/APIToken': '(?P<token>([\w-])+)'"
max_retries = 30
enable_stealth = True

def javascript_fetch(url, auth_token):
    # Less reliable
    return str(driver.execute_script("fetch('" + url + "', { method: 'GET', headers: { 'X-Auth-Token': '"+auth_token+"', },}).then(function(response) { return response.json();}).catch(function(err) { return err; });"))

options = webdriver.ChromeOptions()
if enable_stealth:
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)

if enable_stealth:
    stealth(driver,
        user_agent = UA,
        languages = ["de-DE", "de"],
        vendor  = "Google Inc.",
        platform  = "Win32",
        webgl_vendor  = "Intel Inc.",
        renderer  = "Intel Iris OpenGL Engine",
        fix_hairline  = True,
        run_on_insecure_origins  = False,
    )

# Test stealth
# driver.get("https://bot.sannysoft.com/")
driver.get("http://www.tinder.com")

while True:
    local_storage = str(driver.execute_script("return window.localStorage;"))
    xauth_token = re.search(token_RE, local_storage)
    if xauth_token:
        xauth_token = xauth_token.group("token")
        print(f'FOUND TOKEN {xauth_token} on {driver.current_url}')
 
        # OR JUST CALL tinder_api.py instead       
        get_messages(xauth_token)

        driver.quit()
        break
    elif max_retries < 1:
        driver.quit()
        break
    else:
        time.sleep(10)
        max_retries = max_retries - 1
        print(f'DEBUG \n PAGE: {driver.current_url} \n LOCAL STORAGE: {local_storage}') 

