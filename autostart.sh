#!/bin/bash

# Set wallpaper
swaybg -i  ~/Pictures/the_valley.png -o '*' -m fill >/dev/null 2>&1 &

# Set display configuration
kanshi &

# Notifications
mako &

# Bluetooth
blueman-applet &

# Open Tablet Driver for Graphics tablet
otd-daemon &

# Network manager applet
nm-applet &

#Authentication
/usr/libexec/kf6/polkit-kde-authentication-agent-1 &

# Open Blender in group "2"
ydotoold &

org.blender.Blender &

#ydotool click 0xC0 &
#ydotool key 125:1 42:1 3:1 3:0 42:0 125:0 &

# sleep .5 &

# Lock screen after 30 minuets of inactivity
# After another 30 minutes turn of display
swayidle -w \
	timeout 1800 'swaylock -f -c 000000' \
	timeout 3600 'wlopm --off \*' \
	resume 'wlopm --on \*' \
	before-sleep 'swaylock -f -c 000000' &