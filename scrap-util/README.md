# scrap-util

Command line util, acting like a client for the web scrapping server. It's a study project, nothing more 

### About project
Both client and server implemented with sockets. Client sends HTTP request to the server and server gets page with HTTPS, handles request and respondes.
You need 'keywords.egg-info' to use client as an util, you can make one with setup.py.


### Usage
to run server:
```sh
$ python -m src.server
```
util:
```sh
$ keywords --url *your_url*
```
At the time there is only one 'keywords' command to find most common used words on the page 