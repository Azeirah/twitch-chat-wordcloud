# Introduction

No introduction right now, I'll write one later :)

# Installation

Requirements are:

* PIL (pip install PIL)
* PySide (pip install PySide)
* Python 3.3.5 (untested with other versions)

# Usage

python cloudGui.py

Then: There's a little interface with a few empty boxes
All of them are required.

Fill in the following details

* Twitch chat username: <your twitch chat username>
* Oauth: click [the Oauth link](http://www.twitchapps.com/tmi/), and generate a code, put the code in this box
* Channel name: The name of the twitch chat channel you want to use, you can find the channel name right above the twitch chat on any twitch.tv
* Maximum text length: This is the amount of characters from the chat twitch-wordcloud uses. Use a short number (100 - 2000), and the wordcloud will only be based on recent messages in the chat. The higher the number, the longer the history of the chat will be used to generate the wordcloud. If you want a wordcloud of the past hour, use a huge number like (1000000), if you want to do a short vote, use a medium (5000) or small number (1000-2500) depending on the amount of streamers you have
I want to make this a little more intuitive, this is a little low-level atm.
* Image mask: press the little `...` button to select an image that will be used as the wordcloud's image mask :)
* Refresh rate, how often the wordcloud gets refreshed, in seconds. Really low refresh rates (0.1s) will heavily affect your performance, higher ones (2s+) shouldn't affect performance too much
* Preview cloud below, check this box if you want to see the cloud in the interface, disable it if you just want to use the wordcloud image on your stream, since it affects performance a little bit