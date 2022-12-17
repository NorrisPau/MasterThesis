from selenium import webdriver
from selenium_stealth import stealth
import time
import re
import requests
import uuid

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
token_RE = "'TinderWeb\/APIToken': '(?P<token>([\w-])+)'"
max_retries = 30
enable_stealth = True

def give_me_some_random_id():
    # That's a really nice UUID you have there
    # https://www.youtube.com/watch?v=nSsLNkFoHoU
    return str(uuid.uuid4())

def python_fetch(url, auth_token):
    # More reliable
    # Less stealth
    headers = {'User-Agent': UA,'Accept': 'application/json','Accept-Language': 'en,en-US','Referer': 'https://tinder.com/','app-session-time-elapsed': '2069','app-version': '1035600','tinder-version': '3.56.0','user-session-time-elapsed': '1850','x-supported-image-formats': 'webp,jpeg','platform': 'web','support-short-video': '1','Origin': 'https://tinder.com','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'cross-site','Connection': 'keep-alive',
                'X-Auth-Token': auth_token,
                'app-session-id': give_me_some_random_id(),
                'persistent-device-id': give_me_some_random_id(),
                'user-session-id': give_me_some_random_id(),}
    response = requests.get(url, headers=headers)
    return response

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
        match_data = python_fetch("https://api.gotinder.com/v2/matches?locale=en&count=60&message=0&is_tinder_u=false", xauth_token).json()
        # TODO: Paginate for people with more than 60 Matches
        for match in match_data["data"]["matches"]:
            match_id = match["id"]
            match_name = match["person"]["name"]
            match_messages = python_fetch(f'https://api.gotinder.com/v2/matches/{match_id}/messages?count=100&locale=en', xauth_token).json()
            print(f'{match_id} | {match_name} | {match_messages}')
        driver.quit()
        break
    elif max_retries < 1:
        driver.quit()
        break
    else:
        time.sleep(10)
        max_retries = max_retries - 1
        print(f'DEBUG \n PAGE: {driver.current_url} \n LOCAL STORAGE: {local_storage}') 
