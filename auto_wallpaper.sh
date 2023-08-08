#!/bin/bash

./url_wallpaper.py > url
while read line; do
	echo $line
	curl $line --output wallpaper.jpg; 
done < url
rm url

# Uncommente to set i3 Wallpaper
# mv wallpaper.jpg ~/.background-image
