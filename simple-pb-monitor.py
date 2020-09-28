import requests
import time
import sys
import os
import ssl
import json
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

# Check for command line parameters for the keywords file and output directory
# Start with defaults of ./keywords.txt and .

# Start with defaults
keyword_file = 'keywords.txt'
slack_file_name = 'slack.json'
output_path = '.'
input_path = '.'
check_ip = False
slack_notify = False
slack_token = ''
slack_channel = ''


# keywords file as the first argument after the python file
# Note this is changed in to input path not file in the slack notify changes
if len(sys.argv) > 1:
    input_path = sys.argv[1]

# output directory as the second parameter after the python file
if len(sys.argv) > 2:
    output_path = sys.argv[2]

# Turn on the check for non-authed IP
if len(sys.argv) > 3:
    if 'True' in sys.argv[3]:
        check_ip = True

# Load the keywords
with open(os.path.join(input_path, keyword_file)) as f:
    keywords = f.read().splitlines()

print("keywords ", keywords)

# if slack.json exists the we'll set up notifications
# load parameters from file
slack_file_path = os.path.join(input_path, slack_file_name)
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

    # Added a debug statement if the API is not authed, it has to be enabled through the params though to stop
    # pastes containing the text causing false positives (especially as the response code is 200 regardless)
    if check_ip:
        if "DOES NOT HAVE ACCESS" in str(r.content):
            print(r.content)
            exit(-1)

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

                            # Check whether the directory with the name of the keyword exists and create it if not
                            if not os.path.isdir(output_path+'/'+word):
                                # Create the directory
                                os.mkdir(output_path+'/'+word)

                            # Save to current dir using the key as the filename
                            file_object = open(output_path+'/'+word+'/'+individual['key'], 'w', encoding="utf-8")
                            file_object.write(text)
                            file_object.close()

                            # Notify to slack if enabled
                            if slack_notify:
                                notify(message)

                            # Removed the break because we do want to save multiple times if multiple keywords are
                            # matched because we now have a directory per key word '''

                    # Add to the checklist of the last 1000 so we don't fetch unnecessarily
                    if check_index == 999:
                        print("Resetting the checklist counter")
                        check_index = 0
                    # at the key to the last 1000 check_list and increment the counter
                    check_list.insert(check_index, individual['key'])
                    check_index = check_index + 1
            else:
                print("Skipping {}, already processed".format(individual['key']))

    else:
        print("There was an error calling the url")

    # wait a minute
    print("Sleeping a minute")
    time.sleep(60)



