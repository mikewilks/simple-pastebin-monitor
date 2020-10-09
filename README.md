# simple-pastebin-monitor
A simple pastebin monitor using the scraping API.

Simple pastebin monitor is a simple Python script that replicates and extends Pastebin alerts function. It makes use of the Pastebin Scraping API as described [here](https://pastebin.com/api_scraping_faq). You'll need a Pastebin PRO account to get access to the Scraping API.

Simple pastebin monitor saves the pastes it matches to disk and optionally notifies via a Slack channel.

The script takes two parameters, you need to specify both or neither:
1. The input directory where the keywords.txt file is located (and the optional slack.json)
2. The directory to save the pastes into (default is .)

The script will check Pastebin for pastes every minute and compare their text against the supplied keywords. When there is a match the text of the paste is saved to the output directory (in a directory with the name of the matched keyword) and optionally notified via Slack. This is an improvement over the built-in Pastebin alerts which only saves a link meaning you miss removed pastes if you don't click the link before they are taken down.

Running the script can be done in a screen / tmux or by using the built conatiner image. The machine where you run needs to be have its IP whitelisted in your Pastebin [account](https://pastebin.com/api_scraping_faq). Pre-requisites are Python 3, Requests, slackclient, a Pastebin PRO account and an internet connection.

The notification to a Slack channel is optional and is enabled by the presence of a file called slack.json in the input directory. There is a sample of this file in the repo, it has two parameters containing the Slack token and the channel name to notify in. The Slack token can be obtained by following the 'Add a Bot User' instructions [here](https://slack.com/intl/en-gb/help/articles/115005265703-Create-a-bot-for-your-workspace). The token we need in our config file is the one found in the "Install App" part of the config page in the section "OAuth Tokens for Your Team".


There are various To Dos described in issues on GitHub.

I wrote about about this code on my [blog](http://www.mikewilks.com/home/who-has-your-data)

A Containerised version can be found on [Docker Hub](https://hub.docker.com/r/mikewilks/simple-pastebin-monitor/) or you can pull it from the GitHub Container Registry e.g. docker pull ghcr.io/mikewilks/simple-pastebin-monitor:latest

# Container instructions

There is an automated build pushed to Docker Hub from [GitHub repo](https://github.com/mikewilks/simple-pastebin-monitor).

There is also a GitHub Action creating a container image on the GitHub Container Registry (ghcr.io/mikewilks/simple-pastebin-monitor:latest)

A further image is available on quay.io (quay.io/mikewilks/simple-pastebin-monitor)

The container needs two vols mounting for output and input (containing a keywords.txt of things to search for and optional slack.json). There is a sample of the keywords.txt on GitHub but it is a simple CR separated list.

A simple run command using podman looks like:

`podman run -d --name simple-pastebin-monitor -v /path/to/input-dir-containing-keywords.txt-and-optional-slack.json:/input -v /path/to/store-pastes:/output mikewilks/simple-pastebin-monitor`

or with docker

`sudo docker run -d --name simple-pastebin-monitor -v /path/to/input-dir-containing-keywords.txt-and-optional-slack.json/input -v /path/to/store-pastes:/output mikewilks/simple-pastebin-monitor`

or you can be explicit about the registry (in the example below GitHub Container Registry)

`podman run -d --name simple-pastebin-monitor -v /path/to/input-dir-containing-keywords.txt-and-optional-slack.json:/input -v /path/to/store-pastes:/output ghcr.io/mikewilks/simple-pastebin-monitor`

