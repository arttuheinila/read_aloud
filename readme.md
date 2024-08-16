# Read aloud machine #

A relatively simple python script that reads the text in computer clipboard aloud using Google Text To Speech (gTTS).

I sometimes would like to read a text but am lazy, or want to multitask so I created the program for that.

Or I want part of the webpage read, but not from the start which can be a problem with some products. 

Or the text is not in webbrowser and I still want it read

## Features ##

* Define text language (english or finnish)
At any one time I might have finnish or english text on the clipboard so the code defines the language (based on the first 10 words) and sets the gTTS to read in selected language

* Speed of 1.25 *
I find the normal speed of gTTS to be horribly slow, so I used VLC player with 1.25x to make it work better for me.
Playback with VLC has the added benefit of allowing keyboard interrupt with Ctrl+C during playback if done with the text (which playsound isn't good at)

* Add punctuations at end of line of not present *
My texts might be unordered lists, which typically don't have punctuations at the end. This code adds a punctuation at the end of a line if none present to make gTTS pause in a more natural way.


## Dependencies ##
Install vlc with

pip install python-vlc