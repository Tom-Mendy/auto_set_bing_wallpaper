#!/bin/bash

./auto_set_bing_wallpaper/url_wallpaper.py > url
while read line; do
	echo $line
	curl $line --output wallpaper.jpg; 
done < url
rm url

sudo mv wallpaper.jpg /usr/share/wallpapers/bing_wallpaper.jpg

feh --bg-scale --zoom fill /usr/share/wallpapers/bing_wallpaper.jpg
