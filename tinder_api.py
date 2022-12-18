import time
import re
import requests
import uuid
import argparse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'

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
    time.sleep(1)
    return response

matches = []
match_messages = []

def get_messages(xauth_token):
    print("Fetching Initial Matches")
    # messages = 0 for uncontacted
    match_data = python_fetch("https://api.gotinder.com/v2/matches?locale=en&count=60&message=1&is_tinder_u=false", xauth_token).json()
    for match in match_data["data"]["matches"]:
        matches.append(match)

    # Paginate for people with more than 60 Matches
    while True:
        if "next_page_token" in match_data["data"]:
            next_token = match_data["data"]["next_page_token"]
            print("Getting next page of matches", next_token)
            match_data = python_fetch("https://api.gotinder.com/v2/matches?locale=en&count=60&message=1&is_tinder_u=false&page_token="+next_token, xauth_token).json()
            for match in match_data["data"]["matches"]:
                matches.append(match)
        else:
            break

    for match in matches:
        match_id = match["id"]
        match_name = match["person"]["name"]
        match_message_data = python_fetch(f'https://api.gotinder.com/v2/matches/{match_id}/messages?count=100&locale=en', xauth_token).json()
        match_messages.append({"Person": match, "Messages": match_message_data['data']})
    
    return match_messages

if __name__ == '__main__':

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-t", "--token", help="API TOKEN")
    args = argParser.parse_args()
    print("args=%s" % args)
    print(get_messages(args.token))
