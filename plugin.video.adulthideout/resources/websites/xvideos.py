import re
import xbmc
from ..functions import add_dir, add_link, make_request, fanart, logos
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib.parse as urllib_parse
import logging
from urllib.parse import urlparse

def process_xvideos_content(url, mode=None):
    # changing the base-URl to base-URL + /new/1/
    if "search" not in url and "/new/" not in url:
        url = f"{url}/new/1/"

    content = make_request(url)
    add_dir(
        '[COLOR blue]Search[/COLOR]',
        'xvideos',
        5,
        f'{logos}xvideos.png',
        fanart,
    )
    match = re.compile('<img src=".+?" data-src="([^"]*)"(.+?)<p class="title"><a href="([^"]*)" title="([^"]*)".+?<span class="duration">([^"]*)</span>', re.DOTALL).findall(content)

    # Get the base URL part from the input URL
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"    

    for thumb, dummy, url, name, duration in match:
        name = name.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', '`')
        url = url.replace('THUMBNUM/', '')
        add_link(
            f'{name} [COLOR lime]({duration})[/COLOR]',
            base_url + url,
            4,
            thumb,
            fanart,
        )

    try:
        match = re.compile('<a href="([^"]*)" class="no-page next-page">').findall(content)
        match = [item.replace('&amp;', '&') for item in match]
        add_dir(
            '[COLOR blue]Next  Page  >>>>[/COLOR]',
            base_url + match[0],
            2,
            f'{logos}xvideos.png',
            fanart,
        )
    except:
        pass
    

def play_xvideos_video(url):
    content = make_request(url)
    
    # Suchen Sie die URLs für die verschiedenen Qualitäten
    high_quality = re.search(r"html5player\.setVideoUrlHigh\('(.+?)'\)", content)
    low_quality = re.search(r"html5player\.setVideoUrlLow\('(.+?)'\)", content)
    hls_quality = re.search(r"html5player\.setVideoHLS\('(.+?)'\)", content)
    
    # Testen Sie die Verfügbarkeit der verschiedenen Qualitäten und geben Sie die erste verfügbare Qualität zurück
    if high_quality:
        return high_quality.group(1)
    elif low_quality:
        return low_quality.group(1)
    elif hls_quality:
        return hls_quality.group(1)
    else:
        raise ValueError("No video found")
