import requests, time

# Load the keywords
keyword_file = 'keywords.txt'
blacklist = []
with open(keyword_file) as f:
    keywords = f.read().splitlines()

print ("keywords ",keywords)

check_index = 0
check_list = []

while True :
    print ("Starting a loop")

    # get the jsons from the scraping api
    r = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=100")

    # if it was successful parse
    if r.status_code == 200 :

        # get json from the response
        parsed_json = r.json()

        # loop through the entries
        for individual in parsed_json :
            # Now get the actual pastes if it is not in the last 100 check_list
            if individual['key'] not in check_list :
                p = requests.get (individual['scrape_url'])
                if p.status_code == 200 :
                    text = p.text
                    #loop through the keywords to see if they are in the post
                    for word in keywords :
                        if word.lower() in text.lower() :
                            print ('Matched keyword \'{}\' and will save {}'.format(word, individual['key']))
                            # Save to current dir using the key as the filename
                            file_object = open(individual['key'], 'w')
                            file_object.write(text)
                            file_object.close()

                            # break out so we don't save the paste multiple times if it contains multiple keywords
                            break
                    # Add to the checklist of the last 1000 so we don't fetch unnecessarily
                    if check_index == 999:
                        print("Reseting the checklist counter")
                        check_index = 0
                    # at the key to the last 1000 check_list and increment the counter
                    check_list.insert(check_index,individual['key'])
                    check_index = check_index + 1
            else :
                print ("Skipping {}, already processed".format(individual['key']))

    else :
        print ("There was an error calling the url")

    # wait a minute
    print ("Sleeping a minute")
    time.sleep(60)



