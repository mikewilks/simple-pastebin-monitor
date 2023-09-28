# simple-pastebin-monitor
A simple pastebin monitor using the scraping API.

[![Simple Pastebin Monitor](https://img.youtube.com/vi/7hmGrLyNh18/0.jpg)](http://www.youtube.com/watch?v=7hmGrLyNh18)

Simple pastebin monitor is a simple Python script that replicates and extends Pastebin alerts function. It makes use of the Pastebin Scraping API as described [here](https://pastebin.com/api_scraping_faq). You'll need a Pastebin PRO account to get access to the Scraping API.

Simple pastebin monitor saves the pastes it matches to disk and optionally notifies to multiple mechanisms using [apprise](https://github.com/caronc/apprise).

The script takes two parameters, you need to specify both or neither:
1. The input directory where the keywords.txt file is located (and the optional notifications.json)
2. The directory to save the pastes into (default is .)

The script will check Pastebin for pastes every minute and compare their text against the supplied keywords. When there is a match the text of the paste is saved to the output directory (in a directory with the name of the matched keyword) and optionally notified via Slack. This is an improvement over the built-in Pastebin alerts which only saves a link meaning you miss removed pastes if you don't click the link before they are taken down.

Running the script can be done in a screen / tmux or by using the built container image. The machine where you run needs to be have its IP whitelisted in your Pastebin [account](https://pastebin.com/doc_scraping_api). Pre-requisites are Python 3, Requests, apprise, a Pastebin PRO account and an internet connection.

The notification is optional and is enabled by the presence of a file called notifications.json in the input directory. There is a sample of this file in the repo, it has a list of parameters in the [apprise format](https://github.com/caronc/apprise/wiki). The script will notify to all the mechanisms listed in the file.


There are various To Dos described in issues on GitHub.

I wrote about this code on my [blog](http://www.mikewilks.com/home/who-has-your-data)

A Containerised version can be found on [Docker Hub](https://hub.docker.com/r/mikewilks/simple-pastebin-monitor/) or you can pull it from the GitHub Container Registry or quay.io e.g.

    docker/podman pull ghcr.io/mikewilks/simple-pastebin-monitor:latest 
    
or 

    docker/podman pull quay.io/mikewilks/simple-pastebin-monitor

# Container instructions

There is an automated build pushed to [Docker Hub](https://hub.docker.com/repository/docker/mikewilks/simple-pastebin-monitor) from [GitHub repo](https://github.com/mikewilks/simple-pastebin-monitor).

There is also a GitHub Action creating a container image on the GitHub Container Registry - ghcr.io/mikewilks/simple-pastebin-monitor:latest

A further image is available on quay.io - quay.io/mikewilks/simple-pastebin-monitor

[![SPBM Container Deployment](https://img.youtube.com/vi/g3au0bloiAM/0.jpg)](http://www.youtube.com/watch?v=g3au0bloiAM)

The container needs two vols mounting for output and input (containing a keywords.txt of things to search for and optional notifications.json). There is a sample of the keywords.txt on GitHub but it is a simple CR separated list.

A simple run command using podman looks like:

`podman run -d --name simple-pastebin-monitor -v /path/to/input-dir-containing-keywords.txt-and-optional-notifications.json:/input -v /path/to/store-pastes:/output mikewilks/simple-pastebin-monitor`

or with docker

`sudo docker run -d --name simple-pastebin-monitor -v /path/to/input-dir-containing-keywords.txt-and-optional-snotifications.json/input -v /path/to/store-pastes:/output mikewilks/simple-pastebin-monitor`

or you can be explicit about the registry (in the example below GitHub Container Registry)

`podman run -d --name simple-pastebin-monitor -v /path/to/input-dir-containing-keywords.txt-and-optional-notifications.json:/input -v /path/to/store-pastes:/output ghcr.io/mikewilks/simple-pastebin-monitor`

