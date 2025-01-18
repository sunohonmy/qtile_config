#!/bin/bash

# Compositor
picom -b --config ~/.config/picom/picom1.conf &

# Set wallpaper
#/usr/libexec/xscreensaver/glslideshow -root &
Rwallpaper &
#feh --bg-fill "/home/sunohonmy/Pictures/Wallpapers/32_9/Mount Fuji, Japan II.jpg" &

# Set display configuration
xrandr --mode 5120x1440 --rate 239.63 &

# Notifications
dunst &

# Bluetooth
blueman-applet &

# Open Tablet Driver for Graphics tablet
otd-daemon &

# Network manager applet
nm-applet &

#Authentication
/usr/libexec/kf6/polkit-kde-authentication-agent-1 &

# Blue light filter
gammastep-indicator &

# Screenshot
flameshot &

# Lock screen after 30 minuets of inactivity
# After another 30 minutes turn of display
