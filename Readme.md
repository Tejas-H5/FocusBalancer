# FocusBalancer

This is a python script that is constantly listening to your keystrokes and mouse clicks/scrolls/movements while it is running, and will pause the current media that is playing in the background when you aren't doing anything, and play the current media when you are. If nothing is already playing in the background, it does nothing.

This sounds counter-intuitive, and you might think that it should be the other way around. I thought so too at first, but then when I implemented it, I found that when I stopped typing, it was actually because I was thinking about what I wanted to do next, and this was actually the moment when I needed the video or music to stop playing. And so, it was maximally distracting when the music/podcast stopped when I was typing, and started when I stopped typing.
And the more I use this, the more it makes sense. 
If someone interrupts me to say something, my video automatically pauses. 
If I have to get up to do something, my video automatically pauses.
This idea is turning out to be a lot better than I had initially imagined.
Do note that the media play/pause button as well as the space key are ignored, so you still have the option to resume whatever it is you are currently listening to without having to constantly click something or move the mouse.

Currently this script only works for windows, because it uses the winsdk python package to check if something is playing, and to play/pause that something. It is probably possible to add code to check what the platform is, and use their bindings to do it there, but I don't currently have that problem so I haven't gone about doing that just yet.


Run this script with `python focusBalancer.py`. Install anything you don't already have with `pip`.
Funnily enough, this script doesn't need escalated privileges to run. 
Meaning that, basically any program on your PC that isn't written in python can be using the exact same APIs
in the exact same ways as this script, but for all sorts of other reasons.
Sounds a bit scary, right? (That's because it is)

