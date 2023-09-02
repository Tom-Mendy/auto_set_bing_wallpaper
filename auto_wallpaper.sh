#!/bin/bash

wget "https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=%sen_US" -O xml_page

base_url="https://www.bing.com"
url=$(cat xml_page |cut --delimiter="<" --fields=11 |cut --character=5-)
url="$base_url$url"
rm -f xml_page

echo $line
curl $line --output wallpaper.jpg; 
mv wallpaper.jpg /home/tmendy/.bing_wallpaper.jpg

feh --bg-scale --zoom fill /home/tmendy/.bing_wallpaper.jpg
