"""
    Desi Tashan Kodi Addon
    Copyright (C) 2016 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re, requests

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
_bu = 'http://radiosindia.com/'

MAINLIST = {'01Tamil': _bu + 'tamilradio.html',
            '02Telugu': _bu + 'teluguradio.html',
            '03Malayalam': _bu + 'malayalamradio.html',
            '04Kannada': _bu + 'kannadaradio.html',
            '05Hindi': _bu + 'hindiradio.html',
            '06Punjabi': _bu + 'punjabiradio.html',
            '07Bangla': _bu + 'banglaradio.html',
            '08English': _bu + 'englishradio.html'}

def get_langs():
    """
    Get the list of languages.
    :return: list
    """
    return MAINLIST.keys()
    
def get_stations(iurl):
    """
    Get the list of stations.
    :return: list
    """
    stations = []
    html = requests.get(iurl, headers=mozhdr).text
    mlink = SoupStrainer('div', {'class':'select'})
    mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
    items = mdiv.findAll('div', {'class':re.compile('^grid_')})

    for item in items:
        title = item.find('h3').text
        url = _bu + item.find('a')['href']
        thumb = _bu + item.find('img')['src']
        stations.append((title, thumb, url))
   
    return stations

def list_langs():
    """
    Create the list of categories in the Kodi interface.
    """
    langs = get_langs()
    listing = []
    for lang in sorted(langs):
        list_item = xbmcgui.ListItem(label=lang[2:])
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _fanart})
        iurl = MAINLIST[lang]
        url = '{0}?action=list_stations&iurl={1}'.format(_url, iurl)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_stations(iurl):
    """
    Create the list of movies in the Kodi interface.
    """
    stations = get_stations(iurl)
    listing = []
    for station in stations:
        list_item = xbmcgui.ListItem(label=station[0])
        list_item.setArt({'thumb': station[1],
                          'icon': station[1],
                          'fanart': _fanart})
        list_item.setInfo('music', {'title': station[0]})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&iurl={1}'.format(_url, station[2])
        is_folder = False
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_audio(iurl):
    """
    Play an audio by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=iurl)
    str_url = play_item.getfilename()
    html = requests.get(str_url, headers=mozhdr).text
    try:
        stream_url = re.findall('audio src="(.*?)"',html)[0]
    except:
        stream_url = ''
    if stream_url == '':
        try:
            stream_url = re.findall('source src="(.*?)"',html)[0]
        except:
            pass
    if stream_url == '':
        try:
            stream_url = re.findall('flashvars.serverHost = "(.*?)"',html)[0]
            if 'http' not in stream_url:
                stream_url = 'http://' + stream_url
        except:
            pass
    # Pass the item to the Kodi player.
    play_item.setPath(stream_url)
    #xbmc.Player().play(stream_url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == 'list_stations':
            list_stations(params['iurl'])
        elif params['action'] == 'play':
            play_audio(params['iurl'])
    else:
        list_langs()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
