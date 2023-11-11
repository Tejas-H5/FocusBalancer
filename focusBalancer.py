import keyboard
from pynput import mouse
import threading
import time
import sys

timer_duration_str = input("How much time spent idling would you consider to be too long? \n(type a number, in seconds): ")
# timer_duration_str = "1"
timer_duration = float(timer_duration_str)

# ---- Using some stackoverflow code to detect if media is currently playing. 
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
        print("couldn't detect media state - no session found!")
        return False
    
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status #get media state enum and compare to current main media session state

def isPlaying():
    return mediaIs("PLAYING")

def tryPause():
    session = asyncio.run(getMediaSession())
    if session == None:
        print("couldn't pause - no media session found!")
        return
    session.try_pause_async()

def tryPlay():
    session = asyncio.run(getMediaSession())
    if session == None:
        print("couldn't resume - no media session found!")
        return
    session.try_play_async()


# ---- end external code

app_is_running = True
active_decay_timer = 0
def activate():
    global active_decay_timer
    active_decay_timer = timer_duration

# Start the key detection thread to activate if we pressed any key anywhere
def key_handler():
    global active_decay_timer
    while app_is_running:
        key = keyboard.read_key()

        # Sometimes we just want to listen to that thing in the background, or play that video.
        # So these keys are getting ignored.
        if key != "play/pause media" and key != "space":
            activate()


thread = threading.Thread(target=key_handler, daemon=True)
thread.start()

def on_move(x, y):
    activate()

def on_click(x, y, button, pressed):
    activate()

def on_scroll(x, y, dx, dy):
    activate()

# Also activate whenever we do anything with the mouse. 
# For some reason, this works outside of the application, unlike pyinput's keyboard
mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
mouse_listener.start()

was_active = False
was_playing = False
delta_time = 1 / 30

paused = False

inverted = False
if len(sys.argv) == 2 and sys.argv[1].startswith("i"):
    inverted = True

def input_check_loop():
    global is_active, was_active, was_playing, active_decay_timer
    print("Focus balancer loop started. Use CTRL + C to exit")

    while app_is_running:
        time.sleep(delta_time)

        if paused:
            continue

        if active_decay_timer > 0:
            active_decay_timer -= delta_time

        is_active = active_decay_timer > 0
        if was_active != is_active:
            was_active = is_active
            
            # By default, we pause the video when we are idling, and play it when we aren't.
            # It sounds a bit counter intuitive, see the readme for a dissertation on the topic
            # TODO: make this work for VLC media player
            if (not is_active) != inverted:
                was_playing = isPlaying()
                tryPause()
            else:
                if was_playing:
                    tryPlay()

thread2 = threading.Thread(target=input_check_loop, daemon=True)    
thread2.start()

while True:
    command = input("> ")
    if command.startswith("invert"):
        inverted = not inverted
        print("inverted:", inverted)
    elif command.startswith("pause"):
        paused = not paused
        print("paused:", paused)
    elif command == "exit":
        break
    else:
        print("unknown command -", command)

app_is_running = False
thread.join()
thread2.join()

print("Threads closed. See you next time")