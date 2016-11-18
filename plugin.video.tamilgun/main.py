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
_fanart = _addon.getAddonInfo('fanart')
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

MAINLIST = {'New Movies': 'http://tamilgun.us/categories/new-movies/',
            'HD Movies': 'http://tamilgun.us/categories/hd-movies/',
            'Dubbed Movies': 'http://tamilgun.us/categories/dubbed-movies/',
            'Trailers': 'http://tamilgun.us/categories/trailers/',
            'Comedy': 'http://tamilgun.us/categories/hd-comedys/',
            'Search': 'http://tamilgun.us/?s='}

def GetSearchQuery(sitename):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search ' + sitename)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_text = keyboard.getText()

    return search_text

def get_vidhost(url):
    """
    Trim the url to get the video hoster
    :return vidhost
    """
    parts = url.split('/')[2].split('.')
    vidhost = '%s.%s'%(parts[len(parts)-2],parts[len(parts)-1])
    return vidhost

def resolve_media(url,videos):

    non_str_list = ['olangal.', '#', 'magnet:', 'desihome.co', 'thiruttuvcd',
                    'cineview', 'bollyheaven', 'videolinkz', 'moviefk.co',
                    'imdb.', 'mgid.', 'desihome', 'movierulz.', 'facebook.', 
                    'm2pub', 'abcmalayalam', 'india4movie.co', '.filmlinks4u',
                    'tamilraja.org']

    embed_list = ['cineview', 'bollyheaven', 'videolinkz', 'vidzcode',
                  'embedzone', 'embedsr', 'fullmovie-hd', 'adly.biz',
                  'embedscr', 'embedrip', 'movembed', 'power4link.us',
                  'watchmoviesonline4u', 'nobuffer.info', 'yo-desi.com',
                  'techking.me', 'onlinemoviesworld.xyz', 'cinebix.com']

    if 'pongomovies' in url:
        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='tabs-catch-all')
        links = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        xbmc.log(msg='========== links: ' + str(links), level=xbmc.LOGNOTICE)
        for linksSection in links:
            if 'iframe' in str(linksSection.contents):
                strurl = str(linksSection.find('iframe')['src'])
                resolve_vidurl(strurl,sources)
       
    elif 'filmshowonline.net/media/' in url:
        r = requests.get(url, headers=mozhdr)
        clink = r.text
        cookies = r.cookies
        eurl = re.findall("url: '([^']*)[\d\D]*nonce :", clink)[0]
        enonce = re.findall("nonce : '([^']*)", clink)[0]
        evid = re.findall("nonce : [\d\D]*?link_id: ([\d]*)", clink)[0]
        values = {'echo' : 'true',
                  'nonce' : enonce,
                  'width' : '848',
                  'height' : '480',
                  'link_id' : evid }
        headers = {'User-Agent': mozagent,
                   'Referer': vidurl,
                  'X-Requested-With': 'XMLHttpRequest'}
        emurl = requests.post(eurl, data=values, headers=headers, cookies=cookies).text
        strurl = (re.findall('(http[^"]*)', emurl)[0]).replace('\\', '')
        resolve_vidurl(strurl, sources)

    elif 'filmshowonline.net/videos/' in url:
        clink = requests.get(url, headers=mozhdr).text
        csoup = BeautifulSoup(clink)
        strurl = csoup.find('iframe')['src']
        if 'http' in strurl:
            resolve_vidurl(strurl, sources)
                    
    elif 'tamildbox' in url:
        try:
            link = requests.get(url, headers=mozhdr).text
            mlink = SoupStrainer('div', {'id':'player-embed'})
            dclass = BeautifulSoup(link, parseOnlyThese=mlink)       
            if 'unescape' in str(dclass):
                etext = re.findall("unescape.'[^']*", str(dclass))[0]
                etext = urllib.unquote(etext)
                dclass = BeautifulSoup(etext)
            glink = dclass.iframe.get('src')
            vidhost = get_vidhost(glink)
            videos.append((vidhost,glink))
            mlink = SoupStrainer('div', {'class':'item-content toggled'})
            dclass = BeautifulSoup(link, parseOnlyThese=mlink)
            glink = dclass.p.iframe.get('src')
            vidhost = get_vidhost(glink)
            videos.append((vidhost,glink))
        except:
            pass

    elif any([x in url for x in embed_list]):
        clink = requests.get(url, headers=mozhdr).text
        csoup = BeautifulSoup(clink)
        try:
            for link in csoup.findAll('iframe'):
                strurl = link.get('src')
                if not any([x in strurl for x in non_str_list]):
                    vidhost = get_vidhost(strurl)
                    videos.append((vidhost,strurl))
        except:
            pass

        try:
            plink = csoup.find(class_='main-button dlbutton')
            strurl = plink.get('href')
            if not any([x in strurl for x in non_str_list]):
                vidhost = get_vidhost(strurl)
                videos.append((vidhost,strurl))
        except:
            pass

        try:
            plink = csoup.find(class_='aio-pulse')
            strurl = plink.find('a')['href']
            if not any([x in strurl for x in non_str_list]):
                vidhost = get_vidhost(strurl)
                videos.append((vidhost,strurl))
        except:
            pass

        try:
            plink = csoup.find(class_='entry-content rich-content')
            strurl = plink.find('a')['href']
            if not any([x in strurl for x in non_str_list]):
                vidhost = get_vidhost(strurl)
                videos.append((vidhost,strurl))
        except:
            pass

        try:
            for linksSection in csoup.findAll('embed'):
                strurl = linksSection.get('src')
                if not any([x in strurl for x in non_str_list]):
                    vidhost = get_vidhost(strurl)
                    videos.append((vidhost,strurl))
        except:
            pass
            
    elif not any([x in url for x in non_str_list]):
        vidhost = get_vidhost(url)
        videos.append((vidhost,url))

    return

def get_categories():
    """
    Get the list of categories.
    :return: list
    """
    return MAINLIST.keys()
    
def get_movies(category):
    """
    Get the list of movies.
    :return: list
    """
    movies = []
    if 'http' not in category:
        if category == 'Search':
            search_text = GetSearchQuery('TamilGun')
            search_text = search_text.replace(' ', '+')
            category = MAINLIST[category] + search_text
        else:
            category = MAINLIST[category]
    html = requests.get(category, headers=mozhdr).text
    mlink = SoupStrainer("div", {"class":"col-sm-4 col-xs-6 item"})
    items = BeautifulSoup(html, parseOnlyThese=mlink)
    plink = SoupStrainer("ul", {"class":"pagination"})
    Paginator = BeautifulSoup(html, parseOnlyThese=plink)

    for item in items:
        title = item.h3.text
        url = item.find('a')['href']
        thumb = item.find('img')['src']
        movies.append((title, thumb, url))
    
    if 'next' in str(Paginator):
        nextli = Paginator.find('li', {'class':'next'})
        lastli = Paginator.find('li', {'class':'last'})
        url = nextli.a.get('href')
        lastpg = lastli.a.get('href').split('page/')[1]
        lastpg = lastpg.split('/')[0]
        currpg = Paginator.find('li', {'class':'active'}).text
        title = 'Next Page (Currently in Page %s of %s)' % (currpg,lastpg)
        movies.append((title, _icon, url))
   
    return movies


def get_videos(movie):
    """
    Get the list of videos.
    :return: list
    """
    videos = []
    if 'cinebix.com' in movie:
        resolve_media(movie,videos)
        
    html = requests.get(movie, headers=mozhdr).text
    mlink = SoupStrainer('div', {'class':'videoWrapper player'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

    try:
        links = videoclass.findAll('iframe')
        for link in links:
            url = link.get('src')
            resolve_media(url,videos)

    except:
        pass

    mlink = SoupStrainer('div', {'class':'post-entry'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

    try:
        links = videoclass.findAll('iframe')
        for link in links:
            url = link.get('src')
            resolve_media(url,videos)

    except:
        pass

    try:
        links = videoclass.findAll('a')
        for link in links:
            url = link.get('href')
            resolve_media(url,videos)
                        
    except:
        pass
    
    return videos


def list_categories():
    """
    Create the list of categories in the Kodi interface.
    """
    categories = get_categories()
    listing = []
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setInfo('video', {'title': category})
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _fanart})
        url = '{0}?action=list_category&category={1}'.format(_url, category)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_movies(category):
    """
    Create the list of movies in the Kodi interface.
    """
    movies = get_movies(category)
    listing = []
    for movie in movies:
        list_item = xbmcgui.ListItem(label=movie[0])
        list_item.setArt({'thumb': movie[1],
                          'icon': movie[1],
                          'fanart': movie[1]})
        list_item.setInfo('video', {'title': movie[0]})
        if 'Next Page' in movie[0]:
            url = '{0}?action=list_category&category={1}'.format(_url, movie[2])
        else:
            url = '{0}?action=list_movie&thumb={1}&movie={2}'.format(_url, movie[1], movie[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
 
   
def list_videos(movie,thumb):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """

    videos = get_videos(movie)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'fanart': thumb})
        list_item.setInfo('video', {'title': video[0]})
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
    vid_url = play_item.getfilename()
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
        if params['action'] == 'list_category':
            list_movies(params['category'])
        elif params['action'] == 'list_movie':
            list_videos(params['movie'],params['thumb'])
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
