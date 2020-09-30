import time
import sys
import os
import ssl
import json
import requests
from slack import WebClient
from slack.errors import SlackApiError


def notify(message_to_notify):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    client = WebClient(token=slack_token, ssl=ssl_context)
    try:
        response = client.chat_postMessage(
            channel=slack_channel,
            text=message_to_notify)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Error from Slack API: {e.response['error']}")


# Constants
KEYWORD_FILE_NAME = 'keywords.txt'
SLACK_FILE_NAME = 'slack.json'

# Defaults
output_path = '.'
input_path = '.'
check_ip = False
slack_notify = False
slack_token = ''
slack_channel = ''


# Check for command line parameters for the keywords file and output directory
# keywords file as the first argument after the python file
# Note this is changed into input path not file in the slack notify changes
if len(sys.argv) > 1:
    input_path = sys.argv[1]

# output directory as the second parameter after the python file
if len(sys.argv) > 2:
    output_path = sys.argv[2]

# Load the keywords
with open(os.path.join(input_path, KEYWORD_FILE_NAME)) as f:
    keywords = f.read().splitlines()

print("keywords ", keywords)

# if slack.json exists the we'll set up notifications
# load parameters from file
slack_file_path = os.path.join(input_path, SLACK_FILE_NAME)
if os.path.isfile(slack_file_path):
    slack_file = open(slack_file_path, "r")
    slack_params = json.loads(slack_file.read())
    slack_file.close()
    slack_notify = True
    slack_token = slack_params["slack_bot_key"]
    slack_channel = slack_params["channel"]

check_index = 0
check_list = []

while True:
    print("Starting a loop")

    # get the jsons from the scraping api
    r = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=100")

    # if it was successful parse
    if r.status_code == 200:

        # get json from the response
        parsed_json = r.json()

        # loop through the entries
        for individual in parsed_json:
            # Now get the actual pastes if it is not in the last 1000 check_list
            if individual['key'] not in check_list:
                p = requests.get(individual['scrape_url'])
                if p.status_code == 200:
                    text = p.text
                    # loop through the keywords to see if they are in the post
                    for word in keywords:
                        if word.lower() in text.lower():
                            message = f"Matched keyword {word} and will save {individual['key']}"
                            print(message)

                            # Check whether the directory with the name of the keyword
                            # exists and create it if not
                            if not os.path.isdir(os.path.join(output_path, word)):
                                # Create the directory
                                os.mkdir(os.path.join(output_path, word))

                            # Save to current dir using the key as the filename
                            file_to_write = os.path.join(output_path, word, individual['key'])
                            file_object = open(file_to_write, 'w', encoding="utf-8")
                            file_object.write(text)
                            file_object.close()

                            # Notify to slack if enabled
                            if slack_notify:
                                notify(message)

                            # Removed the break because we do want to save multiple times if
                            # multiple keywords are matched because we now have a directory
                            # per key word

                    # Add to the checklist of the last 1000 so we don't fetch unnecessarily
                    if check_index == 999:
                        print("Resetting the checklist counter")
                        check_index = 0
                    # at the key to the last 1000 check_list and increment the counter
                    check_list.insert(check_index, individual['key'])
                    check_index = check_index + 1
            else:
                print(f"Skipping {individual['key']}, already processed")
    else:
        print("There was an error calling the url, check the IP is authorised on the pastebin site")

    # wait a minute
    print("Sleeping a minute")
    time.sleep(60)
