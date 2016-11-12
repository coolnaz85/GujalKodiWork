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
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import urlresolver

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_icon = _addon.getAddonInfo('icon')


base_url = 'http://www.desitashan.me/'
base_icon = base_url + 'wp-content/uploads/250x31xtashan-e1468311120832.png.pagespeed.ic.iX20cZ67KF.png'

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
    plink = SoupStrainer(class_='fusion-menu')
    soup = BeautifulSoup(html, 'html.parser', parse_only=plink)
    items = soup.find_all(class_='menu-item')
    for item in items:
        if 'fusion-megamenu-menu' not in str(item):
            ch_name = item.text
            try:
                ch_icon = item.find('img')['src']
                if 'http' not in ch_icon:
                    ch_icon = base_url + ch_icon
            except:
                ch_icon = base_icon
            ch_link = item.find('a')['href']
            if ch_link[0] == '/':
                ch_url = base_url[:-1] + ch_link
            else:
                ch_url = base_url + ch_link
            channels.append((ch_name, ch_icon, ch_url))
    
    return channels


def get_shows(channel):
    """
    Get the list of shows.
    :return: list
    """
    shows = []
    html = requests.get(channel).text
    plink = SoupStrainer(class_='fusion-row')
    soup = BeautifulSoup(html, 'html.parser', parse_only=plink)
    items = soup.find_all(class_='fusion-one-fourth')
    for item in items:
        if ('</li>' not in str(item)) and ('</ul>' not in str(item)):
            sh_name = item.text
            try:
                sh_icon = item.find('img')['src']
                if 'http' not in sh_icon:
                    sh_icon = base_url[:-1] + sh_icon
            except:
                sh_icon = base_icon
            sh_link = item.find('a')['href']
            if sh_link[0] == '/':
                sh_url = base_url[:-1] + sh_link
            else:
                sh_url = base_url + sh_link
            shows.append((sh_name, sh_icon, sh_url))
    
    return shows
    

def get_episodes(show):
    """
    Get the list of episodes.
    :return: list
    """
    episodes = []
    html = requests.get(show).text
    plink = SoupStrainer(class_='fusion-row')
    soup = BeautifulSoup(html, 'html.parser', parse_only=plink)
    items = soup.find_all(class_='fusion-one-fourth')
    for item in items:
        ep_name = item.h4.a.text
        if 'written' not in ep_name.lower():
            try:
                ep_icon = item.find('img')['src']
                if 'http' not in ep_icon:
                    ep_icon = base_url[:-1] + ep_icon
            except:
                ep_icon = base_icon
            ep_link = item.find('a')['href']
            if ep_link[0] == '/':
                ep_url = base_url[:-1] + ep_link
            else:
                ep_url = base_url + ep_link
            episodes.append((ep_name, ep_icon, ep_url))
    plink = SoupStrainer(class_='pagination-next')
    soup = BeautifulSoup(html, 'html.parser', parse_only=plink)
    if 'Next' in str(soup):
        ep_icon = _icon
        ep_link = soup.a.get('href')
        if 'category' in ep_link:
            ep_url = base_url[:-1] + ep_link
        else:
            ep_url = show + ep_link
        ep_name = 'Next Page: ' + ep_url.split('page/')[1][:-1]
        episodes.append((ep_name, ep_icon, ep_url))    
    return episodes


def get_videos(episode):
    """
    Get the list of videos.
    :return: list
    """
    videos = []
    html = requests.get(episode).text
    plink = SoupStrainer(class_='vidLinksContent')
    soup = BeautifulSoup(html, 'html.parser', parse_only=plink)
    items = soup.find_all('a')
    for item in items:
        try:
            vid_name = item['title']
        except:
            vid_name = item.text
        vid_url = item['href']
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
        list_item.setArt({'thumb': base_icon,
                          'icon': base_icon,
                          'fanart': base_icon})
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
        url = '{0}?action=list_channel&channel={1}'.format(_url, channel[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)
    

def list_shows(channel):
    """
    Create the list of channels in the Kodi interface.
    """
    shows = get_shows(channel)
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
            url = '{0}?action=list_episode&episode={1}'.format(_url, episode[2])
        else:
            url = '{0}?action=list_show&show={1}'.format(_url, episode[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
    
    
def list_videos(episode):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """

    videos = get_videos(episode)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _icon})
        list_item.setInfo('video', {'title': video[0], 'genre': 'Desi TV'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(_url, video[1])
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def resolve_url(url):
    duration=7500   
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
    else:
        vhtml = requests.get(vid_link).text
        try:
            vplink = SoupStrainer('iframe')
            vsoup = BeautifulSoup(vhtml, 'html.parser', parse_only=vplink)
            vid_url = vsoup.find('iframe')['src']
        except:
            vplink = SoupStrainer('script', {'data-container':'myPlayer'})
            vsoup = BeautifulSoup(vhtml, 'html.parser', parse_only=vplink)
            vid_url = vsoup.find('script')['data-config']
        stream_url = resolve_url(vid_url)
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
            list_shows(params['channel'])
        elif params['action'] == 'list_show':
            list_episodes(params['show'])
        elif params['action'] == 'list_episode':
            list_videos(params['episode'])
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        #list_countries()
        list_channels('Indian')


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
