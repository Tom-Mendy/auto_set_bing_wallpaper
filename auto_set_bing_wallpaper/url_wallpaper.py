#!/usr/bin/python3

#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
import os
import re
import sys

# replace with the actual path to the bing-desktop-wallpaper-changer folder
path_to_Bing_Wallpapers="/path/to/bing-desktop-wallpaper-changer"

try:  # try python 3 import
    from urllib.request import urlopen
    from urllib.request import urlretrieve
    from configparser import ConfigParser
except ImportError:  # fall back to python2
    from urllib import urlretrieve
    from urllib2 import urlopen  
    from ConfigParser import ConfigParser

import xml.etree.ElementTree as ET

BING_MARKETS = [u'ar-XA',
                u'bg-BG',
                u'cs-CZ',
                u'da-DK',
                u'de-AT',
                u'de-CH',
                u'de-DE',
                u'el-GR',
                u'en-AU',
                u'en-CA',
                u'en-GB',
                u'en-ID',
                u'en-IE',
                u'en-IN',
                u'en-MY',
                u'en-NZ',
                u'en-PH',
                u'en-SG',
                u'en-US',
                u'en-XA',
                u'en-ZA',
                u'es-AR',
                u'es-CL',
                u'es-ES',
                u'es-MX',
                u'es-US',
                u'es-XL',
                u'et-EE',
                u'fi-FI',
                u'fr-BE',
                u'fr-CA',
                u'fr-CH',
                u'fr-FR',
                u'he-IL',
                u'hr-HR',
                u'hu-HU',
                u'it-IT',
                u'ja-JP',
                u'ko-KR',
                u'lt-LT',
                u'lv-LV',
                u'nb-NO',
                u'nl-BE',
                u'nl-NL',
                u'pl-PL',
                u'pt-BR',
                u'pt-PT',
                u'ro-RO',
                u'ru-RU',
                u'sk-SK',
                u'sl-SL',
                u'sv-SE',
                u'th-TH',
                u'tr-TR',
                u'uk-UA',
                u'zh-CN',
                u'zh-HK',
                u'zh-TW']

config_file_skeleton ="""[market]
# If you want to override the current Bing market dectection,
# set your preferred market here. For a list of markets, see
# https://msdn.microsoft.com/en-us/library/dd251064.aspx
area =
[directory]
# Download directory path. By default images are saved to
# /home/[user]/[Pictures]/BingWallpapers/
dir_path =
# Limit the size of the downloaded image directory
# Size should be specified in bytes. The minimum 
# limit is the size of 1 image (whatever size that image is)
# Set to negative value for unlimit. Default value is 100MiB
dir_max_size = 
"""


def get_file_uri(filename):
    return 'file://%s' % filename


def get_market():
    """
    Get the desired Bing Market.

    In order of preference, this program will use:
    * Config value market.area from desktop_wallpaper_changer.ini
    * Default locale, in case that's a valid Bing market
    * Fallback value is 'en-US'.

    :return: Bing Market
    :rtype: str
    """
    return 'en-US'


def get_download_path():
    # By default images are saved to '/home/[user]/[Pictures]/BingWallpapers/'
    default_path = check_output("xdg-user-dir PICTURES", shell=True).strip().decode("utf-8") + "/BingWallpapers"

    try:
        config = ConfigParser()
        config.read(get_config_file())
        path = config.get('directory', 'dir_path')

        return path or default_path
    except Exception:
        return default_path


def get_directory_limit():
    """
    Get the directory sized limit
    """
    config = ConfigParser()
    config.read(get_config_file())
    try:
        size = config.getint('directory', 'dir_max_size')
        return size
    except Exception:
        return 100 * 1024 * 1024


def get_bing_xml():
    """
    Get BingXML file which contains the URL of the Bing Photo of the day.

    :return: URL with the Bing Photo of the day.
    """
    # idx = Number days previous the present day.
    # 0 means today, 1 means yesterday
    # n = Number of images previous the day given by idx
    # mkt = Bing Market Area, see get_valid_bing_markets.
    market = get_market()
    return "https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=%s" % market


def get_screen_resolution_str():
    """
    Get a regexp like string with your current screen resolution.

    :return: String with your current screen resolution.
    """
    sizes = [[800, [600]], [1024, [768]], [1280, [720, 768]],
             [1366, [768]], [1920, [1080, 1200]]]
    sizes_mobile = [[768, [1024]], [720, [1280]],
                    [768, [1280, 1366]], [1080, [1920]]]
    sizew = 1920
    sizeh = 1080
    return r'%sx%s' % (sizew, sizeh)


def get_image_metadata():
    """
    Get Bing wallpaper metadata.

    :return: XML tag object for the wallpaper image.
    """
    bing_xml_url = get_bing_xml()
    page = urlopen(bing_xml_url)

    bing_xml = ET.parse(page).getroot()

    # For extracting complete URL of the image
    images = bing_xml.findall('image')
    return images[0]


def get_image_url(metadata):
    """
    Get an appropriate Wallpaper URL based on your screen resolution.

    :param metadata: XML tag object with image metadata.
    :return: URL with Bing Wallpaper image.
    """
    base_image = metadata.find("url").text
    # Replace image resolution with the correct resolution
    # from your main monitor
    screen_size = get_screen_resolution_str()
    correct_resolution_image = re.sub(r'\d+x\d+', screen_size, base_image)
    return "https://www.bing.com" + correct_resolution_image


def init_dir(path):
    """
    Create directory if it doesn't exist.

    :param path: Path to a directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def p2_dirscan(path):
    files = list()
    size = 0

    for e in os.listdir(path):
        entry = path + "/" + e
        if os.path.isfile(entry) and os.path.splitext(entry)[1] == ".jpg":
            s = os.path.getsize(entry)
            files.append((entry, s))
            size = size + s
    files = sorted(files)
    return files, size

def main():
    """
    Main application entry point.
    """
    app_name = 'Bing Desktop Wallpaper'
    exit_status = 0

    try:
        image_metadata = get_image_metadata()
        image_name = image_metadata.find("startdate").text + ".jpg"
        image_url = get_image_url(image_metadata)
        print(image_url)

    except Exception as err:
        summary = 'Error executing %s' % app_name
        body = err
        print(body)
        exit_status = 1
    
    exit(exit_status)


if __name__ == '__main__':
    main()
