#!/bin/bash

cd /home/tmendy/my_scripts/auto_set_bing_wallpaper/
./url_wallpaper.py > url
while read line; do
	echo $line
	curl $line --output wallpaper.jpg; 
done < url
mv wallpaper.jpg /home/tmendy/bing_wallpaper.jpg
cd $OLDPWD

feh --bg-scale --zoom fill /home/tmendy/bing_wallpaper.jpg
