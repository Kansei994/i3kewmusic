#!/usr/bin/env python3

import os
import sys
import subprocess

player = "kew"

def run_playerctl(*args):
    try:
        return subprocess.check_output(['playerctl', '-p', player, *args], stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        sys.exit()

try:
    # Handle clicks
    if os.environ.get('BLOCK_BUTTON'):
        btn = os.environ['BLOCK_BUTTON']
        if btn == '2':
            subprocess.call(['playerctl', '-p', player, 'previous'], stderr=subprocess.DEVNULL)
        elif btn == '1':
            subprocess.call(['playerctl', '-p', player, 'play-pause'], stderr=subprocess.DEVNULL)
        elif btn == '3':
            subprocess.call(['playerctl', '-p', player, 'next'], stderr=subprocess.DEVNULL)

        # Send signal to refresh i3blocks
        os.system("pkill -RTMIN+3 i3blocks")

    # Get metadata
    artist = run_playerctl('metadata', 'xesam:artist')
    title = run_playerctl('metadata', 'xesam:title')
    status = run_playerctl('status')

    # Format display string
    if status.lower() == 'paused':
        info = "Paused -"
    else:
        info = "Playing -"

    # Python 2/3 compatibility
    if sys.version_info > (3, 0):
        print(f"{info} {artist} - {title}")
    else:
        print((info + " " + artist + " - " + title).encode('utf-8'))

    sys.exit()

except Exception:
    sys.exit()
