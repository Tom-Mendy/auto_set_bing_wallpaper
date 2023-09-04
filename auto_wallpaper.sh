#!/bin/bash

#get image url
wget "https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=%sen_US" -O xml_page
base_url="https://www.bing.com"
url=$(cat xml_page |cut --delimiter="<" --fields=11 |cut --character=5-)
url="$base_url$url"
rm -f xml_page

#dowload image
echo $url
curl $url --output wallpaper.jpg; 
mv wallpaper.jpg /home/tmendy/.bing_wallpaper.jpg

#use feh to set image as wallpaper
feh --bg-scale --zoom fill /home/tmendy/.bing_wallpaper.jpg
