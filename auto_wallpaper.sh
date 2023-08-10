#!/bin/bash

./url_wallpaper.py > url
while read line; do
	echo $line
	curl $line --output wallpaper.jpg; 
done < url
rm url

mv wallpaper.jpg /usr/share/wallpapers/bing_wallpaper.jpg
