import keyboard
from pynput import mouse
import threading
import time

# ---- external code: 
# https://stackoverflow.com/questions/59636713/check-if-audio-playing-with-python-on-windows-10
# https://stackoverflow.com/questions/69610231/why-cant-pip-find-winrt

import asyncio, winsdk.windows.media.control as wmc

async def getMediaSession():
    sessions = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = sessions.get_current_session()
    return session

def mediaIs(state):
    session = asyncio.run(getMediaSession())
    if session == None:
        return False
    
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status #get media state enum and compare to current main media session state

def isPlaying():
    return mediaIs("PLAYING")

def tryPause():
    session = asyncio.run(getMediaSession())
    if session != None:
        session.try_pause_async()

def tryPlay():
    session = asyncio.run(getMediaSession())
    if session != None:
        session.try_play_async()

def setMediaState(state):
    # TODO
    pass

# ---- end external code


app_is_running = True
is_active = 0
def activate():
    global is_active
    is_active = 1

last_is_active = False
was_playing = False
delta_time = 1 / 60
deactivate_speed = 1

# Start the key detection thread to set is_active if we pressed any key anywhere
def key_handler():
    global is_active
    while app_is_running:
        key = keyboard.read_key()
        activate()

thread = threading.Thread(target=key_handler, daemon=True)
thread.start()


def on_move(x, y):
    activate()

def on_click(x, y, button, pressed):
    activate()

def on_scroll(x, y, dx, dy):
    activate()

# Collect events until released
mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
mouse_listener.start()
    

# main loop
print("Main loop started. Use CTRL + C to exit")
while True:
    time.sleep(delta_time)

    if is_active > 0:
        is_active -= deactivate_speed * delta_time

    this_is_active = is_active > 0
    if last_is_active != this_is_active:
        last_is_active = this_is_active
        
        # Very counter intuitive, but we actually want to 
        # pause the video when we aren't typing, and play the video when we are typing.
        # See the readme for more info
        if not this_is_active:
            was_playing = isPlaying()
            tryPause()
        else:
            if was_playing:
                tryPlay()

# this code doesn't get reached lmao. But ideally it should
app_is_running = False
thread.join()