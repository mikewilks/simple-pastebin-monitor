"""Simple Pastebin Monitor"""
import json
import os
import sys
import time
import apprise
import requests


# constants
KEYWORD_FILE_NAME = 'keywords.txt'
NOTIF_FILE_NAME = 'notifications.json'

# defaults
output_path = '.'
input_path = '.'
check_ip = False
notify = False
apobj = ''

# check for command line parameters for the keywords file and output directory
# keywords file as the first argument after the python file
if len(sys.argv) > 1:
    input_path = sys.argv[1]

# output directory as the second parameter after the python file
if len(sys.argv) > 2:
    output_path = sys.argv[2]

# load the keywords
with open(os.path.join(input_path, KEYWORD_FILE_NAME)) as f:
    keywords = f.read().splitlines()

print("keywords ", keywords)

# if notifications.json exists then we'll set up notifications
# load parameters from file
notifications_file_path = os.path.join(input_path, NOTIF_FILE_NAME)
if os.path.isfile(notifications_file_path):
    notifications_file = open(notifications_file_path, "r")
    notifications_params = json.loads(notifications_file.read())
    notifications_file.close()

    # set up the apprise object
    apobj = apprise.Apprise()
    for url in notifications_params['notification_urls']:
        apobj.add(url)
    notify = True

check_index = 0
check_list = []

while True:
    print("starting a loop")

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

                            # Notify if enabled
                            if notify:
                                apobj.notify(body=message, title="Pastebin Monitor")
                                print("Notified")

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
