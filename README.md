# simple-pastebin-monitor
A simple pastebin monitor using the scraping API (and now updated for the new scrpaing URL)

A simple Python script that replicates and and extends Pastbin alerts. Makes use of the Pastebin Scraping API as described here https://pastebin.com/api_scraping_faq. A Pastebin PRO lifetime account is needed to get access the Scraping API (but they are only a few dollars).

The script will check Pastebin for pastes every minute and compare their text against the supplied keywords. When there is a match the text of the paste is saved this is an improvement over the built in alerts which only saves a link so removed pastes are missed if you don't click the link before they are taken down.

Running the script is easiest in a Linux screen or tmux and needs to be from the location of the whitelisted IP in your Pastebin account. Pre-requisites are really just Python 3, a Pastebin PRO lifetime account and an internet connection.

Various To Dos are described in issues 

I blogged about this code here: http://www.mikewilks.com/home/who-has-your-data
