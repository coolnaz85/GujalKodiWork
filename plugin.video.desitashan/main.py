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
import urlresolver

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_icon = _addon.getAddonInfo('icon')


base_url = 'http://www.desitashan.me/'

MAINLIST = {'Indian': base_url,
           'Pakistani': base_url + 'pakistan-tv/'}

def get_countries():
    """
    Get the list of countries.
    :return: list
    """
    return MAINLIST.keys()

    
def get_channels(country):
    """
    Get the list of channels.
    :return: list
    """
    channels = []
    html = requests.get(MAINLIST[country]).text
    mlink = SoupStrainer('div', {'class':'nav fusion-mobile-tab-nav'})
    soup = BeautifulSoup(html, parseOnlyThese=mlink)
    items = soup.findAll('li')
    for item in items:
        title = item.text
        tref = item.a.get('href')[1:]
        try:
            icon = item.find('img')['src']
            if icon.startswith('/'):
                icon = base_url[:-1] + icon
            else:
                icon = base_url + icon
        except:
            icon = _icon
        
        channels.append((title,icon,tref))
    
    return channels


def get_shows(channel,country):
    """
    Get the list of shows.
    :return: list
    """
    shows = []
    html = requests.get(MAINLIST[country]).text
    mlink = SoupStrainer('div', {'id':channel})
    soup = BeautifulSoup(html, parseOnlyThese=mlink)
    items = soup.findAll('div', {'class':'fusion-column-wrapper'})
    for item in items:
        title = item.text
        url = item.a.get('href')
        if url.startswith('/'):
            url = base_url[:-1] + url
        else:
            url = base_url + url
        try:
            icon = item.find('img')['src']
            if icon.startswith('/'):
                icon = base_url[:-1] + icon
            else:
                icon = base_url + icon
        except:
            icon = base_icon
        
        shows.append((title,icon,url))
    
    return shows
    

def get_episodes(show):
    """
    Get the list of episodes.
    :return: list
    """
    episodes = []
    html = requests.get(show).text
    mlink = SoupStrainer('div', {'id':'showList'})
    soup = BeautifulSoup(html, parseOnlyThese=mlink)
    items = soup.findAll('div', {'class':'fusion-column-wrapper'})
    for item in items:
        title = item.h4.a.text
        if 'written' not in title.lower():
            url = item.a.get('href')
            if url.startswith('/'):
                url = base_url[:-1] + url
            else:
                url = base_url + url
            try:
                icon = item.find('img')['src']
                if icon.startswith('/'):
                    icon = base_url[:-1] + icon
                else:
                    icon = base_url + icon
            except:
                icon = base_icon           
            episodes.append((title,icon,url))
    plink = SoupStrainer('a', {'class':'pagination-next'})
    soup = BeautifulSoup(html, parseOnlyThese=plink)
    if 'Next' in str(soup):
        icon = _icon
        ep_link = soup.a.get('href')
        if 'category' in ep_link:
            url = base_url[:-1] + ep_link
        else:
            url = show + ep_link
        title = 'Next Page: ' + url.split('page/')[1][:-1]
        episodes.append((title, icon, url))    
    return episodes


def get_videos(episode):
    """
    Get the list of videos.
    :return: list
    """
    videos = []
    html = requests.get(episode).text
    mlink = SoupStrainer('p', {'class':'vidLinksContent'})
    soup = BeautifulSoup(html, parseOnlyThese=mlink)
    items = soup.findAll('a')
    for item in items:
        try:
            vid_name = item['title']
        except:
            vid_name = item.text
        vid_url = item['href']
        videos.append((vid_name, vid_url))

    mlink = SoupStrainer('div', {'class':'post-content'})
    soup = BeautifulSoup(html, parseOnlyThese=mlink)
    #items = soup.findAll('div', {'class':'video-shortcode'})
    items = soup.findAll('iframe')
    for item in items:
        try:
            vid_name = item['title']
        except:
            vid_name = item['class']
        vid_url = item['src']
        videos.append((vid_name, vid_url))   
        
    return videos


def list_countries():
    """
    Create the list of countries in the Kodi interface.
    """
    countries = get_countries()
    listing = []
    for country in countries:
        list_item = xbmcgui.ListItem(label=country+' Channels')
        list_item.setInfo('video', {'title': country, 'genre': country})
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _icon})
        url = '{0}?action=list_country&country={1}'.format(_url, country)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_channels(country):
    """
    Create the list of countries in the Kodi interface.
    """
    channels = get_channels(country)
    listing = []
    for channel in channels:
        list_item = xbmcgui.ListItem(label=channel[0])
        list_item.setArt({'thumb': channel[1],
                          'icon': channel[1],
                          'fanart': channel[1]})
        list_item.setInfo('video', {'title': channel[0], 'genre': country})
        url = '{0}?action=list_channel&channel={1}&country={2}'.format(_url, channel[2], country)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)
    

def list_shows(channel,country):
    """
    Create the list of channels in the Kodi interface.
    """
    shows = get_shows(channel,country)
    listing = []
    for show in shows:
        list_item = xbmcgui.ListItem(label=show[0])
        list_item.setArt({'thumb': show[1],
                          'icon': show[1],
                          'fanart': show[1]})
        list_item.setInfo('video', {'title': show[0], 'genre': 'Desi TV'})
        url = '{0}?action=list_show&show={1}'.format(_url, show[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

    
def list_episodes(show):
    """
    Create the list of episodes in the Kodi interface.
    """
    episodes = get_episodes(show)
    listing = []
    for episode in episodes:
        list_item = xbmcgui.ListItem(label=episode[0])
        list_item.setArt({'thumb': episode[1],
                          'icon': episode[1],
                          'fanart': episode[1]})
        list_item.setInfo('video', {'title': episode[0], 'genre': 'Desi TV'})
        if 'Next Page' not in episode[0]:
            url = '{0}?action=list_episode&episode={1}&icon={2}'.format(_url, episode[2], episode[1])
        else:
            url = '{0}?action=list_show&show={1}'.format(_url, episode[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
    
    
def list_videos(episode,icon):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """

    videos = get_videos(episode)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': icon,
                          'icon': icon,
                          'fanart': icon})
        list_item.setInfo('video', {'title': video[0], 'genre': 'Desi TV'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(_url, video[1])
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def resolve_url(url):
    duration=5000   
    try:
        stream_url = urlresolver.HostedMediaFile(url=url).resolve()
        # If urlresolver returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = url
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
            return False
    except Exception as e:
        try: msg = str(e)
        except: msg = url
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
        return False
        
    return stream_url


def play_video(path):
    """
    Play a video by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_link = play_item.getfilename()
    #xbmc.log(msg = '=======> Item is : %s'%url, level = xbmc.LOGNOTICE)
    if '/coming/' in vid_link:
        stream_url = 'http://www.tashanplayer.com/upcoming.mp4'
    elif 'tashanplayer' in vid_link:
        vhtml = requests.get(vid_link).text
        try:
            vplink = SoupStrainer('iframe')
            vsoup = BeautifulSoup(vhtml, parseOnlyThese=vplink)
            vid_url = vsoup.find('iframe')['src']
        except:
            vplink = SoupStrainer('script', {'data-container':'myPlayer'})
            vsoup = BeautifulSoup(vhtml, parseOnlyThese=vplink)
            vid_url = vsoup.find('script')['data-config']
        stream_url = resolve_url(vid_url)
    else:
        stream_url = resolve_url(vid_link)
    play_item.setPath(stream_url)
    # Pass the item to the Kodi player.
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
        if params['action'] == 'list_country':
            list_channels(params['country'])
        elif params['action'] == 'list_channel':
            list_shows(params['channel'],params['country'])
        elif params['action'] == 'list_show':
            list_episodes(params['show'])
        elif params['action'] == 'list_episode':
            list_videos(params['episode'],params['icon'])
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_countries()
        #list_channels('Indian')


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
