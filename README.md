# simple-pastebin-monitor
A simple pastebin monitor using the scraping API (and now updated for the new scraping URL)

Simple Pastebin Monitor is a simple Python script that replicates and and extends Pastebin alerts. It makes use of the Pastebin Scraping API as described [here](https://pastebin.com/api_scraping_faq). You'll need a Pastebin PRO account to get access to the Scraping API).

The script takes three parameters, you need to specify all or none:
1. The name and location of the file containing the keywords to check (default is ./keywords.txt)
2. The directory to save the pastes into (default is .)
3. Whether to check for the pastebin message that your IP is not authorized or not (default is false)

The script will check Pastebin for pastes every minute and compare their text against the supplied keywords. When there is a match the text of the paste is saved to the output directory (in a directory with the name of the matched keyword). This is an improvement over the built in Pastebin alerts which only saves a link which means you miss removed pastes if you don't click the link before they are taken down.

Running the script can be done in a screen / tmux or by using the built docker image. The machine where you run needs to be have its IP whitelisted in your Pastebin [account](https://pastebin.com/api_scraping_faq). Pre-requisites are really just Python 3, Requests, a Pastebin PRO account and an internet connection.

There are various To Dos are described in issues on GitHub but these are probably a way off.

I wrote about about this code on my [blog](http://www.mikewilks.com/home/who-has-your-data)

A Containerized version can be found on [Docker Hub](https://hub.docker.com/r/mikewilks/simple-pastebin-monitor/)

# Docker instructions

The container needs two vols mounting for output and input (containing a keywords.txt of things to search for). There is a sample of the keywords.txt on GitHub but it is a simple CR separated list.

A simple docker run command looks like:

`docker run -d --name simple-pastebin-monitor -v /path/to/dir-containing-keywords.txt:/input -v /path/to/store-pastes:/output mikewilks/simple-pastebin-monitor`

This is an automated build from a [GitHub repo](https://github.com/mikewilks/simple-pastebin-monitor)
