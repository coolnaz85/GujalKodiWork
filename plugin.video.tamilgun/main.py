"""
    Tamilgun Kodi Addon
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
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re, requests, urllib, json
import jsunpack
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

    non_str_list = ['#', 'magnet:', 'desihome.co', 'thiruttuvcd',
                    'cineview', 'bollyheaven', 'videolinkz',
                    'imdb.', 'mgid.', 'facebook.', 'm2pub', 
                    'tamilraja.org']

    embed_list = ['cineview', 'bollyheaven', 'videolinkz', 'vidzcode',
                  'embedzone', 'embedsr', 'fullmovie-hd', 'adly.biz',
                  'embedscr', 'embedrip', 'movembed', 'power4link.us',
                  'techking.me', 'onlinemoviesworld.xyz', 'cinebix.com']

    if 'tamildbox' in url:
        link = requests.get(url, headers=mozhdr).text
        try:
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
        
        try:
            codes = re.findall('"return loadEP.([^,]*),(\d*)',link)
            for ep_id, server_id in codes:
                burl = 'http://www.tamildbox.com/actions.php?case=loadEP&ep_id=%s&server_id=%s'%(ep_id,server_id)
                bhtml = requests.get(burl,headers=mozhdr).text
                blink = re.findall('(?i)iframe\s*src="(.*?)"',bhtml)[0]
                vidhost = get_vidhost(blink)
                if 'googleapis' in blink:
                    blink = 'https://drive.google.com/open?id=' + re.findall('docid=([^&]*)',blink)[0]
                    vidhost = 'GVideo'
                videos.append((vidhost,blink))   
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
    bu = 'http://tamilgun.pro'
    r = requests.get(bu, headers=mozhdr)
    if r.url != bu:
        bu = r.url
    items = {}
    cats = re.findall('id="menu-item-[^4].*?href="((?=.*categories).*?)">((?!User).*?)<',r.text)
    sno = 1
    for cat in cats:
        items[str(sno)+cat[1]] = cat[0]
        sno+=1
    items[str(sno)+'[COLOR yellow]** Search **[/COLOR]'] = bu + '/?s='
    return items
    
def get_movies(iurl):
    """
    Get the list of movies.
    :return: list
    """
    movies = []
    
    if iurl[-3:] == '?s=':
        search_text = GetSearchQuery('TamilGun')
        search_text = urllib.quote_plus(search_text)
        iurl += search_text

    html = requests.get(iurl, headers=mozhdr).text
    mlink = SoupStrainer('article', {'class':re.compile('video')})
    items = BeautifulSoup(html, parseOnlyThese=mlink)
    plink = SoupStrainer('ul', {'class':'page-numbers'})
    Paginator = BeautifulSoup(html, parseOnlyThese=plink)

    for item in items:
        title = item.h3.text
        url = item.h3.find('a')['href']
        try:
            thumb = item.find('img')['src'].strip()
        except:
            thumb = _icon
        movies.append((title, thumb, url))
    
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'class':re.compile('next')})
        purl = nextli.get('href')
        if 'http' not in purl:
            purl = self.bu[:-12] + purl
        currpg = Paginator.find('span', {'class':re.compile('current')}).text
        pages = Paginator.findAll('a', {'class':re.compile('^page')})
        lastpg = pages[len(pages)-1].text
        title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
        movies.append((title, _icon, purl))
   
    return movies


def get_videos(url):
    """
    Get the list of videos.
    :return: list
    """
    videos = []
    if 'cinebix.com' in url:
        resolve_media(url,videos)
        return videos
        
    html = requests.get(url, headers=mozhdr).text

    try:
        linkcode = jsunpack.unpack(html).replace('\\','')
        sources = json.loads(re.findall('sources:(.*?)\}\)',linkcode)[0])
        for source in sources:    
            url = source['file'] + '|Referer=http://%s/'%get_vidhost(source['file'])
            url = urllib.quote_plus(url)
            videos.append(('tamilgun | %s'%source['label'],url))
    except:
        pass

    mlink = SoupStrainer('div', {'id':'videoframe'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
    try:
        links = videoclass.findAll('iframe')
        for link in links:
            url = link.get('src')
            resolve_media(url,videos)
    except:
        pass

    mlink = SoupStrainer('div', {'class':'entry-excerpt'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
    try:
        links = videoclass.findAll('iframe')
        for link in links:
            if 'http' in str(link):
                url = link.get('src')
                resolve_media(url,videos)
    except:
        pass

    try:
        url = videoclass.p.a.get('href')
        resolve_media(url,videos)
    except:
        pass    
    
    try:
        sources = json.loads(re.findall('vdf-data-json">(.*?)<',html)[0])
        url = 'https://www.youtube.com/watch?v=%s'%sources['videos'][0]['youtubeID']
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
    for title,iurl in sorted(categories.iteritems()):
        list_item = xbmcgui.ListItem(label=title[1:])
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _fanart})
        url = '{0}?action=list_category&category={1}'.format(_url, urllib.quote(iurl))
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
    if 'tamilgun' not in vid_url:
        stream_url = resolve_url(vid_url)
        if stream_url:
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
