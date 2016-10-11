"""
    Deccan Delight Kodi Addon
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

import os, re, sys, urllib, json, xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
from t0mm0.common.addon import Addon
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import urlresolver
   
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer


# plugin constants
__plugin__ = 'plugin.video.deccandelight'
__author__ = 'Gujal'
_DD = Addon(__plugin__, sys.argv)
Addon = xbmcaddon.Addon(id=__plugin__)
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

# plugin settings
SETTINGS_CACHE_TIMEOUT = _DD.get_setting('Cache-Timeout')
SETTINGS_ADULT = _DD.get_setting('EnableAdult')
SETTINGS_ENABLEOPENSSL = _DD.get_setting('EnableOpenSSL')
SETTINGS_TamilGun = _DD.get_setting('TamilGun_enabled')
SETTINGS_RajTamil = _DD.get_setting('RajTamil_enabled')
SETTINGS_TamilYogi = _DD.get_setting('TamilYogi_enabled')
SETTINGS_RunTamil = _DD.get_setting('RunTamil_enabled')
SETTINGS_APKLand = _DD.get_setting('APKLand_enabled')
SETTINGS_TamilTVS = _DD.get_setting('TamilTVS_enabled')
SETTINGS_ABCMal = _DD.get_setting('ABCMal_enabled')
SETTINGS_Olangal = _DD.get_setting('Olangal_enabled')
SETTINGS_LiveMal = _DD.get_setting('LiveMal_enabled')
SETTINGS_HLinks = _DD.get_setting('HLinks_enabled')
SETTINGS_YoDesi = _DD.get_setting('YoDesi_enabled')
SETTINGS_TVCD = _DD.get_setting('TVCD_enabled')
SETTINGS_KitMovie = _DD.get_setting('KitMovie_enabled')
SETTINGS_TTwists = _DD.get_setting('TTwists_enabled')
SETTINGS_MRulz = _DD.get_setting('MRulz_enabled')
SETTINGS_FLinks = _DD.get_setting('FLinks_enabled')
SETTINGS_MovieFK = _DD.get_setting('MovieFK_enabled')
SETTINGS_I4M = _DD.get_setting('I4M_enabled')
SETTINGS_MFish = _DD.get_setting('MFish_enabled')
SETTINGS_RedM = _DD.get_setting('RedM_enabled')
SETTINGS_Mersal = _DD.get_setting('Mersal_enabled')
SETTINGS_TVCDs = _DD.get_setting('TVCDs_enabled')

import requests

cache = StorageServer.StorageServer("deccandelight", SETTINGS_CACHE_TIMEOUT)
logo = os.path.join(_DD.get_path(), 'icon.png')
currPage = 0
search_text = ''
paginationText = ''
mode = _DD.queries['mode']
play = _DD.queries.get('play', None)
RootDir = _DD.get_path()
dlg = xbmcgui.DialogProgress()
cwd = _DD.get_path()
img_path = cwd + '/resources/images/'
abcm_img = img_path + 'abcmalayalam.png'
flinks_img = img_path + 'flinks.png'
moviefk_img = img_path + 'moviefk.png'
mfish_img = img_path + 'mfish.png'
hlinks_img = img_path + 'hlinks.png'
kmovie_img = img_path + 'kmovie.png'
mersal_img = img_path + 'mersal.png'
mrulz_img = img_path + 'mrulz.png'
olangal_img = img_path + 'olangal.png'
rajt_img = img_path + 'rajtamil.png'
rmovies_img = img_path + 'rmovies.png'
tgun_img = img_path + 'tamilgun.png'
runt_img = img_path + 'runt.png'
ttwist_img = img_path + 'ttwist.png'
tvcd_img = img_path + 'thiruttuvcd.png'
tvcds_img = img_path + 'tvcds.png'
ttvs_img = img_path + 'apkland.png'
lmtv_img = img_path + 'lmtv.png'
yamgo_img = img_path + 'yamgo.png'
i4m_img = img_path + 'i4m.png'
yd_img = img_path + 'yodesi.png'
tts_img = img_path + 'tts.png'
tyogi_img = img_path + 'tyogi.png'
next_img = img_path + 'next.png'
fan_img = cwd + '/fanart.jpg'
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
mozagent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def GetSearchQuery(sitename):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search ' + sitename)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_text = keyboard.getText()

    return search_text

def mov_menu(keylist):
    ok=True

    keylist = keylist
    keylist.sort()
    MovTitle_Str=""    
    fanarturl_Str=""
    
    for key, value in Dict_res.iteritems():
        if 'Paginator' not in value:
            SplitValues = value.split(",")
            try:
                for eachSplitVal in SplitValues:
                    eachSplitVal = eachSplitVal.encode('utf8')
                    if 'mode' in eachSplitVal:
                        mode_Str = str(eachSplitVal.replace('mode=', '')).strip()
                    elif 'url' in eachSplitVal:
                        fullLink_Str = str(eachSplitVal.replace('url=', '')).strip()
                    elif 'imgLink' in eachSplitVal:
                        fanarturl_Str = str(eachSplitVal.replace('imgLink=', '')).strip()
                    elif 'MovTitle' in eachSplitVal:
                        MovTitle_Str = str(eachSplitVal.replace('MovTitle=', '')).strip()
            
                if MovTitle_Str:
                    _DD.add_directory({'mode': mode_Str, 'url': fullLink_Str, 'fanarturl': fanarturl_Str , 'title': MovTitle_Str}, {'title': MovTitle_Str}, img=fanarturl_Str, fanart=fan_img)
            except:
                print "No likely exception caught"                        
    try:
        PaginatorVal = Dict_res['Paginator']
        if PaginatorVal:
            SplitValues = PaginatorVal.split(",")
            for eachSplitVal in SplitValues:
                eachSplitVal = eachSplitVal.encode('utf8')
                if 'mode' in eachSplitVal:
                    mode_Str = str(eachSplitVal.replace('mode=', '')).strip()
                elif 'currPage' in eachSplitVal:
                    currPage_Str = str(eachSplitVal.replace('currPage=', '')).strip()
                elif 'subUrl' in eachSplitVal:
                    subUrl_Str = str(eachSplitVal.replace('subUrl=', '')).strip()
                elif 'title' in eachSplitVal:
                    title_Str = str(eachSplitVal.replace('title=', '')).strip()
                elif 'search_text' in eachSplitVal:
                    search_Str = str(eachSplitVal.replace('search_text=', '')).strip()
            _DD.add_directory({'mode': mode_Str, 'subUrl': subUrl_Str, 'currPage': currPage_Str, 'search_text': search_Str }, {'title': title_Str}, img=next_img, fanart=fan_img)

    except:
        print "No Pagination found"

    return ok

def clean_movtitle(movTitle):
    hyph = u'\u2013'.encode('utf8')
    movTitle = movTitle.encode('utf8')
    movTitle = movTitle.replace(hyph, '')
    movTitle = movTitle.replace('(In Hindi)', '')
    movTitle = movTitle.replace('Documentary', '')
    movTitle = movTitle.replace('Hot Hindi Movie', '')
    movTitle = movTitle.replace('Malayalam', '')
    movTitle = movTitle.replace(' Tamil', '')
    movTitle = movTitle.replace('MALAYALAM', '')
    movTitle = movTitle.replace('Movies', '')
    movTitle = movTitle.replace('Movie', '')
    movTitle = movTitle.replace('movie', '')
    movTitle = movTitle.replace('Film', '')
    movTitle = movTitle.replace('film', '')
    movTitle = movTitle.replace('New', '')
    movTitle = movTitle.replace('MOVIE', '')
    movTitle = movTitle.replace('MP4', '')
    movTitle = movTitle.replace('Full', '')
    movTitle = movTitle.replace('FULL', '')
    movTitle = movTitle.replace('Length', '')
    movTitle = movTitle.replace('Glamour', '')
    movTitle = movTitle.replace('Masala', '')
    movTitle = movTitle.replace('Latest', '')
    movTitle = movTitle.replace('Romantic', '')
    movTitle = movTitle.replace('Releases', '')
    movTitle = movTitle.replace('Hot ', '')
    movTitle = movTitle.replace(' And ', '')
    movTitle = movTitle.replace('|', '')
    movTitle = movTitle.replace('.', '')
    movTitle = movTitle.replace('Sex ', '')
    movTitle = movTitle.replace('Adults', '')
    movTitle = movTitle.replace(' hot ', '')
    movTitle = movTitle.replace('Hindi', '')
    movTitle = movTitle.replace('Bollywood', '')
    movTitle = movTitle.replace('full', '')
    movTitle = movTitle.replace('Watch', '')
    movTitle = movTitle.replace('Online', '')
    movTitle = movTitle.replace('online', '')
    movTitle = movTitle.replace('Telugu', '')
    movTitle = movTitle.replace('Length', '')
    movTitle = movTitle.replace('[18+]', '')
    movTitle = movTitle.replace('[+18]', '') 
    movTitle = movTitle.replace('18+', '')   
    movTitle = movTitle.replace('For Free', '')
    movTitle = movTitle.replace(' Free', '')
    movTitle = movTitle.replace('watch', '')
    movTitle = movTitle.replace('Download', '')
    movTitle = movTitle.replace('download', '')
    movTitle = movTitle.replace('-', '')
    movTitle = movTitle.replace('/', '')
    movTitle = movTitle.replace('DVDSCR', '')
    movTitle = movTitle.replace('DVDScr', '')
    movTitle = movTitle.replace('DVDscr', '')
    movTitle = movTitle.replace('DVDRip', '')
    movTitle = movTitle.replace('DVDRIP', '')
    movTitle = movTitle.replace('WEBRip', '')
    movTitle = movTitle.replace('WebRip', '')
    movTitle = movTitle.replace('DTHRip', '')
    movTitle = movTitle.replace('TCRip', '')
    movTitle = movTitle.replace('HDRip', '')
    movTitle = movTitle.replace('HDTVRip', '')
    movTitle = movTitle.replace('HD-TC', '')
    movTitle = movTitle.replace('HDTV', '')
    movTitle = movTitle.replace('TVRip', '')
    movTitle = movTitle.replace('TS', '')
    movTitle = movTitle.replace('tamil ', '')
    movTitle = movTitle.replace('Dubbed', '')
    movTitle = movTitle.replace('Super ', '')
    movTitle = movTitle.replace('Hilarious', '')
    movTitle = movTitle.replace('Ultimate', '')
    movTitle = movTitle.replace('Best', '')
    movTitle = movTitle.replace('Classy ', '')
    movTitle = movTitle.replace(' comedy ', '')
    movTitle = movTitle.replace('Comedy', '')
    movTitle = movTitle.replace('Video', '')
    movTitle = movTitle.replace('Scenes', '')
    movTitle = movTitle.replace('Scene', '')
    movTitle = movTitle.replace('Songs', '')
    movTitle = movTitle.replace('songs', '')
    movTitle = movTitle.replace('Punjabi ', '')
    movTitle = movTitle.replace('punjabi ', '')
    movTitle = movTitle.replace('DVD', '')
    movTitle = movTitle.replace('VDSCR', '')
    movTitle = movTitle.replace('Bluray', '')
    movTitle = movTitle.replace('*', '')
    movTitle = movTitle.replace('BluRay', '')
    movTitle = movTitle.replace('Kannada', '')
    movTitle = movTitle.replace('Pakistani', '')
    movTitle = movTitle.replace(' English', '')
    movTitle = movTitle.replace(' HD', '')
    movTitle = movTitle.replace('720p', '')
    movTitle = movTitle.replace('scenes', '')
    movTitle = movTitle.replace('Collection', '')
    movTitle = movTitle.replace('Hollywood', '')
    movTitle = movTitle.replace('Short ', '')
    movTitle = movTitle.replace('Biography', '')
    movTitle = movTitle.replace('Bengali', '')
    movTitle = movTitle.replace('Bhojpuri', '')
    movTitle = movTitle.replace('Gujarati', '')
    movTitle = movTitle.replace('Marathi', '')
    movTitle = movTitle.replace('Nepali', '')
    movTitle = movTitle.replace('Oriya', '')
    movTitle = movTitle.replace('Panjabi', '')
    movTitle = movTitle.replace('Rajasthani', '')
    movTitle = movTitle.replace('Urdu', '')
    movTitle = movTitle.strip()
    return movTitle

def resolve_vidurl(url,sources):
    if 'google.' in url:
        url = url.replace('/preview', '/edit')
        glink = requests.get(url, headers=mozhdr, verify=False).text
        strurl = (re.findall('"fmt_stream_map.*?(http[^|]*)', glink)[0]).replace('\\u0026', '&').replace('\\u003d', '=')
        hmf = 'url : ' + strurl

    else:
        hmf = urlresolver.HostedMediaFile(url)
        
    if hmf:
        sources.append(hmf)
    else:
        xbmc.log(msg = url + ' not resolvable by urlresolver!', level = xbmc.LOGNOTICE)

    return sources
    
def resolve_media(vidurl,sources):

    non_str_list = ['olangal.', '#', 'magnet:', 'desihome.co', 'thiruttuvcd',
                    'cineview', 'bollyheaven', 'videolinkz', 'moviefk.co',
                    'imdb.', 'mgid.', 'desihome', 'movierulz.', 'facebook.', 
                    'm2pub', 'abcmalayalam', 'india4movie.co', '.filmlinks4u']

    embed_list = ['cineview', 'bollyheaven', 'videolinkz', 'vidzcode',
                  'embedzone', 'embedsr', 'fullmovie-hd', 'adly.biz',
                  'embedscr', 'embedrip', 'movembed', 'power4link.us',
                  'watchmoviesonline4u', 'nobuffer.info', 'yo-desi.com',
                  'techking.me', 'onlinemoviesworld.xyz']

    if 'pongomovies' in vidurl:
        link = requests.get(vidurl, headers=mozhdr).text
        mlink = SoupStrainer(class_='tabs-catch-all')
        links = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        xbmc.log(msg='========== links: ' + str(links), level=xbmc.LOGNOTICE)
        for linksSection in links:
            if 'iframe' in str(linksSection.contents):
                strurl = str(linksSection.find('iframe')['src'])
                resolve_vidurl(strurl,sources)
       
    elif 'filmshowonline.net/media/' in vidurl:
        r = requests.get(vidurl, headers=mozhdr)
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

    elif 'filmshowonline.net/videos/' in vidurl:
        clink = requests.get(vidurl, headers=mozhdr).text
        csoup = BeautifulSoup(clink)
        strurl = csoup.find('iframe')['src']
        if 'http' in strurl:
            resolve_vidurl(strurl, sources)
                    
    elif 'tamildbox' in vidurl:
        try:
            link = requests.get(vidurl, headers=mozhdr).text
            mlink = SoupStrainer(id='player-embed')
            dclass = BeautifulSoup(link, 'html.parser', parse_only=mlink)       
            if 'unescape' in str(dclass):
                etext = re.findall("unescape.'[^']*", str(dclass))[0]
                etext = urllib.unquote(etext)
                dclass = BeautifulSoup(etext)
            glink = dclass.iframe.get('src')
            resolve_vidurl(glink, sources)
            mlink = SoupStrainer(class_='item-content')
            dclass = BeautifulSoup(link, 'html.parser', parse_only=mlink)
            glink = dclass.p.iframe.get('src')
            resolve_vidurl(glink, sources)
        except:
            print 'no embedded urls found using tamildbox method'

    elif any([x in vidurl for x in embed_list]):
        clink = requests.get(vidurl, headers=mozhdr).text
        csoup = BeautifulSoup(clink)
        try:
            for linksSection in csoup.findAll('iframe'):
                strurl = linksSection.get('src')
                if not any([x in strurl for x in non_str_list]):
                    resolve_vidurl(strurl, sources)

        except:
            print " : no iframe urls found using embedurl method"

        try:
            plink = csoup.find(class_='main-button dlbutton')
            strurl = plink.get('href')
            if not any([x in strurl for x in non_str_list]):
                resolve_vidurl(strurl, sources)

        except:
            print " : no urls found using button method"

        try:
            plink = csoup.find(class_='aio-pulse')
            strurl = plink.find('a')['href']
            if not any([x in strurl for x in non_str_list]):
                resolve_vidurl(strurl, sources)

        except:
            print " : no urls found using second button method"

        try:
            plink = csoup.find(class_='entry-content rich-content')
            strurl = plink.find('a')['href']
            if not any([x in strurl for x in non_str_list]):
                resolve_vidurl(strurl, sources)

        except:
            print " : no urls found using rich-content method"

        try:
            for linksSection in csoup.findAll('embed'):
                strurl = linksSection.get('src')
                if not any([x in strurl for x in non_str_list]):
                    resolve_vidurl(strurl, sources)

        except:
            print " : no embed urls found using embedurl method"
            
    elif not any([x in vidurl for x in non_str_list]):
        resolve_vidurl(vidurl, sources)

    return sources

def list_media(movTitle, sources, fanarturl):
    ok = True
    sources = urlresolver.filter_source_list(sources)
    for idx, s in enumerate(sources):
        if 'google.' in str (s):
            url = re.findall('(http.*)', str(s))[0]
            vidhost = 'docs.google.com'
        else:
            url =  s.get_url()
            vidhost = re.findall('//(.*?)/', url)[0]
            vidhost = re.findall('(?:.*\.|)(.*\..+)', vidhost)[0]
        li = xbmcgui.ListItem(vidhost)
        #li.setContentLookup(enable=False)
        li.setArt({ 'fanart': fanarturl,
                    'thumb': fanarturl })
        #li.setInfo( type="Video", infoLabels={ "Title": movTitle } )
        li_url = _DD.build_plugin_url({'url': url, 'play': 'True'})
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), li_url, li, isFolder=False)
        
    return ok

def resolve_url(url):
    duration=7500   
    try:
        stream_url = urlresolver.HostedMediaFile(url=url).resolve()
        # If urlresolver returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = url
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, __icon__))
            return False
    except Exception as e:
        try: msg = str(e)
        except: msg = url
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, __icon__))
        return False
        
    return stream_url

def getMovList_thiruttuvcd(thiruttuvcd_url):

    Dict_movlist = {}

    if 'thiruttumasala' in thiruttuvcd_url:
        url = thiruttuvcd_url      
        base_url = 'http://www.thiruttumasala.com'
        headers = {'User-Agent': mozagent,
                   'Accept-Encoding': 'deflate'}	
        link = requests.get(url, headers=headers).text
        soup = BeautifulSoup(link)
        ItemNum=0
        for eachItem in soup.findAll('div', { 'class':'video_box' }):
            ItemNum=ItemNum+1
            links = eachItem.find_all('a')
            for link in links:
                if link.has_attr('href'):
                    link = link.get('href')
            img = eachItem.find('img')['src']
            movTitle = eachItem.find('img')['alt']
            Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + base_url + link + ', imgLink=' + base_url + img+', MovTitle='+movTitle})

        Paginator = soup.find(class_='pagination')
        currPage = Paginator.find('span', { 'class':'currentpage' })
        CurrentPage = int(currPage.string)
        paginationText = ''
        for eachPage in Paginator.findAll('a'):
            if ('Next' not in eachPage.contents[0]) and ('Prev' not in eachPage.contents[0]):
                lastPage = int(eachPage.string)
               
        if (CurrentPage < lastPage):
            paginationText = '(Currently in Page ' + str(CurrentPage) + ' of ' + str(lastPage) + ')\n'
        
        if '/search' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_msearch'
        else:
            subUrl = 'thiruttuvcd_masala'
        if paginationText:
            Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    else:
        url = thiruttuvcd_url
        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link)
        ItemNum=0
        for eachItem in soup.findAll('div', { 'class':'postbox' }):
            ItemNum=ItemNum+1
            links = eachItem.find_all('a')
            for link in links:
                if link.has_attr('href'):
                    link = link.get('href')
            img = eachItem.find('img')['src']
            movTitle = eachItem.find('img')['alt']
            movTitle = clean_movtitle(movTitle)
            Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + link + ', imgLink=' + img+', MovTitle='+movTitle.decode('utf8')})

        paginationText = ''
        CurrPage = soup.find('span', { 'class':'pages' })
        if CurrPage:
            txt = CurrPage.text
            re1 = '.*?'  # Non-greedy match on filler
            re2 = '(\\d+)'  # Integer Number 1
            rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
            m = rg.search(txt)
            if m:
                int1 = m.group(1)
                CurrentPage = int(int1)
                paginationText = "(Currently in " + txt + ")\n"

        if 'tamil-movies' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_tamilMovs'
        elif 'malayalam/' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_MalayalamMovs'
        elif 'telugu-movie' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_teluguMovs'
        elif 'hindi-movies' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_hindiMovs'
        elif 'hot-movies' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_adult'
        elif '/tv/' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_tamiltv'
        elif '/?s=' in thiruttuvcd_url:
            subUrl = 'thiruttuvcd_search'
            
        if paginationText:
            Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})
        
    return Dict_movlist

def getMovList_tvcds(tvcds_url):

    Dict_movlist = {}

    url = tvcds_url
    link = requests.get(url, headers=mozhdr).text
    mlink = SoupStrainer(class_='boxentry')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0
    for eachItem in Items:
        ItemNum = ItemNum+1
        movPage = eachItem.find('a')['href']
        imgSrc = eachItem.find('img')['src']
        movTitle = eachItem.find('a')['title']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'})
        lastPage = laPage.string
        lPage = int(re.findall('of (.*)', lastPage)[0])

        if (CurrentPage < lPage):
            paginationText = '(Currently in ' + lastPage + ')\n'
        
    if 'tamil-movies' in tvcds_url:
        subUrl = 'tvcds_tamil'
    elif '/english/' in tvcds_url:
        subUrl = 'tvcds_english'
    elif '/telugu/' in tvcds_url:
        subUrl = 'tvcds_telugu'
    elif '/hindi/' in tvcds_url:
        subUrl = 'tvcds_hindi'
    elif '/private/' in tvcds_url:
        subUrl = 'tvcds_adult'
    elif '?s=' in tvcds_url:
        subUrl = 'tvcds_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})
    
    return Dict_movlist

def getMovList_rajtamil(rajTamilurl):

    Dict_movlist = {}
    link = requests.get(rajTamilurl, headers=mozhdr).text
    soup = BeautifulSoup(link)
    ItemNum=0
    for eachItem in soup.findAll('li'):
        for coveritem in eachItem.findAll("div", { "class":"post-thumb"}):
            links = coveritem.find_all('a')
            for link in links:
                ItemNum=ItemNum+1
                movTitle = link['title']
                movTitle = clean_movtitle(movTitle)
                movPage = link['href']
            try:
                imgSrc = coveritem.find('img')['src']
            except:
                imgSrc = rajt_img

            Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    Paginator = soup.find("div", { "class":"navigation"})
    paginationText=''
    currPage = Paginator.find("span", { "class":"page-numbers current"})
    if currPage:
        CurrentPage = int(currPage.string)

        for eachPage in Paginator.findAll("a", { "class":"page-numbers"}):
            if "Next" not in eachPage.contents[0] and "Prev" not in eachPage.contents[0]:
                lastPage = int(eachPage.string)
                
        if (CurrentPage < lastPage):
            paginationText = "( Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"

        
    if 'comedy' in rajTamilurl:
        subUrl = 'rajtamilcomedy'
    elif 'songs' in rajTamilurl:
        subUrl = 'rajtamilsongs'
    elif 'tamil-dubbed' in rajTamilurl:
        subUrl = 'rajtamildubbed'
    elif 'vijay-tv-shows' in rajTamilurl:
        subUrl = 'rajtamilTVshowsVijayTV'
    elif 'sun-tv-show' in rajTamilurl:
        subUrl = 'rajtamilTVshowsSunTV'
    elif '/?s=' in rajTamilurl:
        subUrl = 'rajtamilsearch'
    else:
        subUrl = 'rajtamilRecent'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_mersal(mersalurl):
    Dict_movlist = {}
    link = requests.get(mersalurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='col-sm-6 col-md-4 col-lg-4')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0
    for eachItem in Items:
        ItemNum = ItemNum+1
        movTitle = eachItem.find('img')['title']
        movPage = 'http://mersalaayitten.com' + eachItem.find('a')['href']
        try:
            imgSrc = eachItem.find('img')['data-original']
        except:
            imgSrc = eachItem.find('img')['src']
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc+', MovTitle='+movTitle})

    mlink = SoupStrainer(class_='pagination pagination-lg')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText = ''
    try:
        currPage = Paginator.find("li", { "class":"active"})
    except:
        currPage = ''
    if currPage:
        CurrentPage = int(currPage.span.string)

        for eachPage in Paginator.findAll("li", { "class":"hidden-xs"}):
            lastPage = int(eachPage.a.string)

        if (CurrentPage < lastPage):
            paginationText = "(Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"

    if 'c=1' in mersalurl:
        subUrl = 'mersal_Tamil'
    elif 'c=2' in mersalurl:
        subUrl = 'mersal_Hindi'
    elif 'c=3' in mersalurl:
        subUrl = 'mersal_Telugu'
    elif 'c=4' in mersalurl:
        subUrl = 'mersal_Malayalam'
    elif 'c=5' in mersalurl:
        subUrl = 'mersal_Animation'
    elif 'c=6' in mersalurl:
        subUrl = 'mersal_Dubbed'
    elif 'search_query=' in mersalurl:
        subUrl = 'mersal_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_mrulz(mrulzurl):
    Dict_movlist = {}
    link = requests.get(mrulzurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='cont_display')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0
    for eachItem in Items:
        ItemNum = ItemNum+1
        movTitle = (eachItem.find('a')['title'])
        movTitle = clean_movtitle(movTitle)
        movPage = eachItem.find('a')['href']
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = mrulz_img

        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='nav-older')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText = ''
    if '/page/' in str(Paginator):
        pageurl = Paginator.find('a')['href']
        npage = re.findall('/page/(\\d*)', pageurl)[0]
        CurrentPage = int(npage) - 1
        paginationText = "(Currently in Page " + str(CurrentPage) + ")\n"

    if 'tamil-dubbed' in mrulzurl:
        subUrl = 'mrulz_tdubbed'
    elif 'telugu-dubbed' in mrulzurl:
        subUrl = 'mrulz_tgdubbed'
    elif 'tamil-' in mrulzurl:
        subUrl = 'mrulz_Tamil'
    elif 'telugu-' in mrulzurl:
        subUrl = 'mrulz_Telugu'
    elif 'kannada-' in mrulzurl:
        subUrl = 'mrulz_Kannada'
    elif 'punjabi-' in mrulzurl:
        subUrl = 'mrulz_Punjabi'
    elif 'bengali-' in mrulzurl:
        subUrl = 'mrulz_Bengali'
    elif 'adult-' in mrulzurl:
        subUrl = 'mrulz_adult'
    elif 'hindi-dubbed' in mrulzurl:
        subUrl = 'mrulz_hdubbed'
    elif 'malayalam-' in mrulzurl:
        subUrl = 'mrulz_Mal'
    elif 'bollywood-movie-2016' in mrulzurl:
        subUrl = 'mrulz_h2016'
    elif 'bollywood-movie-2015' in mrulzurl:
        subUrl = 'mrulz_h2015'
    elif 'bollywood-movie-2014' in mrulzurl:
        subUrl = 'mrulz_h2014'
    elif 'hollywood-movie-2016' in mrulzurl:
        subUrl = 'mrulz_e2016'
    elif 'hollywood-movie-2015' in mrulzurl:
        subUrl = 'mrulz_e2015'
    elif 'hollywood-movie-2014' in mrulzurl:
        subUrl = 'mrulz_e2014'
    elif '/?s=' in mrulzurl:
        subUrl = 'mrulz_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_rmovies(rmoviesurl):
    Dict_movlist = {}
    link = requests.get(rmoviesurl, headers=mozhdr).text
    soup = BeautifulSoup(link,'html5lib')
    Items = soup.find_all(class_='thumb')
    ItemNum = 0
    for eachItem in Items:
        ItemNum = ItemNum+1
        imgSrc = eachItem.find('img')['src']
        movPage = eachItem.find('a')['href']
        movTitle = eachItem.find('a')['title']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    Paginator = soup.find(class_='wp-pagenavi')
    paginationText=''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'})
        lastPage = laPage.string
        lPage = int(re.findall('of (.*)', lastPage)[0])

        if (CurrentPage < lPage):
            paginationText = '(Currently in ' + lastPage + ')\n'

    if '/tamil' in rmoviesurl:
        subUrl = 'rmovies_Tamil'
    elif '/telugu' in rmoviesurl:
        subUrl = 'rmovies_Telugu'
    elif '/malayalam' in rmoviesurl:
        subUrl = 'rmovies_Malayalam'
    elif '/kannada' in rmoviesurl:
        subUrl = 'rmovies_Kannada'
    elif '/punjabi' in rmoviesurl:
        subUrl = 'rmovies_Punjabi'
    elif '/dubbed' in rmoviesurl:
        subUrl = 'rmovies_Dubbed'
    elif '/bollywood' in rmoviesurl:
        subUrl = 'rmovies_Hindi'
    elif '/hollywood' in rmoviesurl:
        subUrl = 'rmovies_English'
    elif '/animation' in rmoviesurl:
        subUrl = 'rmovies_Animated'
    elif '/pakistan' in rmoviesurl:
        subUrl = 'rmovies_Urdu'
    elif '/adult' in rmoviesurl:
        subUrl = 'rmovies_Adult'
    elif '/?s=' in rmoviesurl:
        subUrl = 'rmovies_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_moviefk(moviefkurl):
    Dict_movlist = {}
    link = requests.get(moviefkurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='singlepost')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0
    for eachItem in Items:
        ItemNum = ItemNum+1
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = moviefk_img
        movPage = eachItem.find('a')['href']
        movTitle = eachItem.find('a')['title']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'})
        lastPage = laPage.string

        if (CurrentPage < lastPage):
            paginationText = "(Currently in " + lastPage + ")\n"

    if '/tamil' in moviefkurl:
        subUrl = 'moviefk_Tamil'
    elif '/telugu' in moviefkurl:
        subUrl = 'moviefk_Telugu'
    elif '/marathi' in moviefkurl:
        subUrl = 'moviefk_Marathi'
    elif '/punjabi' in moviefkurl:
        subUrl = 'moviefk_Punjabi'
    elif '/hindi-dubbed' in moviefkurl:
        subUrl = 'moviefk_Dubbed'
    elif '/hindi' in moviefkurl:
        subUrl = 'moviefk_Hindi'
    elif '/hollywood' in moviefkurl:
        subUrl = 'moviefk_English'
    elif '/wwe' in moviefkurl:
        subUrl = 'moviefk_WWE'
    elif '/?s=' in moviefkurl:
        subUrl = 'moviefk_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=%s, currPage=%s,title=Next Page.. %s,search_text=%s'%(subUrl,CurrentPage+1,paginationText,search_text)})

    return Dict_movlist

def getMovList_tamilgun(tamilgunurl):

    Dict_movlist = {}
    link = requests.get(tamilgunurl, headers=mozhdr).text
    soup = BeautifulSoup(link,'html5lib')
    Items = soup.find_all(class_='col-sm-4 col-xs-6 item')
    ItemNum = 0

    for eachItem in Items:
        ItemNum = ItemNum+1
        movTitle = eachItem.h3.a.string
        movTitle = clean_movtitle(movTitle)
        movPage = eachItem.find('a')['href']
        imgSrc = eachItem.find('img')['src']
        if 'http' not in imgSrc:
            imgSrc = 'http:' + imgSrc
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc+', MovTitle='+movTitle.decode('utf8')})

    Paginator = soup.find(class_='pagination')
    currPage = Paginator.find("li", { "class":"active"})
    CurrentPage = int(currPage.a.string)
    lastPage = CurrentPage
    lPage = Paginator.find("li", { "class":"last"})
    if lPage:
        laPage = lPage.find('a')['href']
        lastPage = re.findall('page/(\\d*)', laPage)[0]
    
    if (CurrentPage < lastPage):
        paginationText = "(Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"
    else:
        paginationText = ""

    if 'new-movies' in tamilgunurl:
        subUrl = 'tamilgunnew'
    elif 'dubbed-movies' in tamilgunurl:
        subUrl = 'tamilgundubbed'
    elif 'hd-movies' in tamilgunurl:
        subUrl = 'tamilgunhd'
    elif 'hd-comedys' in tamilgunurl:
        subUrl = 'tamilguncomedy'
    elif 'trailers' in tamilgunurl:
        subUrl = 'tamilguntrailer'
    elif '/?s=' in tamilgunurl:
        subUrl = 'tamilgunsearch'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_tyogi(tyogiurl):

    Dict_movlist = {}
    link = requests.get(tyogiurl, headers=mozhdr).text
    #mlink = SoupStrainer(class_='cover')
    #Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    soup = BeautifulSoup(link, 'html5lib')
    Items = soup.find_all(class_='cover')
    ItemNum = 0

    for eachItem in Items:
        ItemNum = ItemNum+1
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = tyogi_img
        movPage = eachItem.find('a')['href']
        movTitle = eachItem.find('img')['alt']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    #mlink = SoupStrainer(class_='navigation')
    #Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    Paginator = soup.find(class_='navigation')
    paginationText = ""
    if 'current' in str(Paginator):
        currPage = Paginator.find(class_='page-numbers current')
        CurrentPage = int(currPage.string)
        lastPage = CurrentPage
        for eachPage in Paginator.findAll('a', { 'class':'page-numbers' }):
            if "next" not in str(eachPage) and "prev" not in str(eachPage):
                lastPage = int(eachPage.string)
    
    if (CurrentPage < lastPage):
        paginationText = "(Currently in Page %s of %s)"%(CurrentPage,lastPage)
    else:
        paginationText = ""

    if '-full-movie-' in tyogiurl:
        subUrl = 'tyogi_new'
    elif '-dubbed-movies-' in tyogiurl:
        subUrl = 'tyogi_dubbed'
    elif '-bluray-movies' in tyogiurl:
        subUrl = 'tyogi_hd'
    elif '-dvdrip-movies' in tyogiurl:
        subUrl = 'tyogi_dvd'
    elif '/?s=' in tyogiurl:
        subUrl = 'tyogisearch'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=%s, currPage=%s,title=Next Page.. %s,search_text=%s'%(subUrl,CurrentPage+1,paginationText,search_text)})

    return Dict_movlist

def getMovList_runtamil(runtamilurl):

    Dict_movlist = {}
    link = requests.get(runtamilurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='movie-poster')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0

    for eachItem in Items:
        ItemNum = ItemNum+1
        movTitle = eachItem.find('img')['alt']
        movTitle = clean_movtitle(movTitle)
        movPage = eachItem.find('a')['href']
        imgSrc = eachItem.find('img')['src']
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc+', MovTitle='+movTitle.decode('utf8')})

    paginationText = ''
    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText = ''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find(class_='pages').text
        CurrentPage = int(re.findall('Page\s?(\d*)', currPage)[0])
        lastPage = int(re.findall('of\s?(\d*)', currPage)[0])

        if (CurrentPage < lastPage):
            paginationText = '(Currently in %s)\n'%(currPage)

    if 'new-tamil' in runtamilurl:
        subUrl = 'runtamilnew'
    elif 'old-tamil' in runtamilurl:
        subUrl = 'runtamilold'
    elif 'tamil-dubbed' in runtamilurl:
        subUrl = 'runtamildubbed'
    elif 'hd-movies' in runtamilurl:
        subUrl = 'runtamilhd'
    elif 'dvd-movies' in runtamilurl:
        subUrl = 'runtamildvd'
    elif '/?s=' in runtamilurl:
        subUrl = 'runtamilsearch'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_ttwist(ttwisturl):

    Dict_movlist = {}
    link = requests.get(ttwisturl, headers=mozhdr).text
    mlink = SoupStrainer(class_='listing-videos listing-wall')
    lsoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0
    Items = lsoup.findAll(class_='border-radius-5 box-shadow')
    for eachItem in Items:
        ItemNum = ItemNum+1
        #movTitle = eachItem.find('h2').find('a').string
        movTitle = eachItem.find('a')['title']
        movTitle = clean_movtitle(movTitle)
        movPage = eachItem.find('a')['href']
        imgSrc = eachItem.find('img')['src']
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc+', MovTitle='+movTitle.decode('utf8')})

    mlink = SoupStrainer(class_='pagination')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText = ""
    if 'current' in str(Paginator):
        currPage = Paginator.find(class_='page-numbers current')
        CurrentPage = int(currPage.string)
        lastPage = CurrentPage
        for eachPage in Paginator.findAll('a', { 'class':'page-numbers' }):
            if "next" not in str(eachPage) and "prev" not in str(eachPage):
                lastPage = int(eachPage.string)
        
        if (CurrentPage < lastPage):
            paginationText = "(Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"


    if 'new-movies' in ttwisturl:
        subUrl = 'ttwistnew'
    elif 'dubbed-movies' in ttwisturl:
        subUrl = 'ttwistdubbed'
    elif 'hd-movies' in ttwisturl:
        subUrl = 'ttwisthd'
    elif 'malayalam-movies' in ttwisturl:
        subUrl = 'ttwistmal'
    elif 'telugu-movies' in ttwisturl:
        subUrl = 'ttwisttel'
    elif 'hindi-movies' in ttwisturl:
        subUrl = 'ttwisthin'
    elif 'hot-masala' in ttwisturl:
        subUrl = 'ttwistadult'
    elif 'trailers' in ttwisturl:
        subUrl = 'ttwisttrailer'
    elif '/?s=' in ttwisturl:
        subUrl = 'ttwistsearch'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_flinks(flinksurl):

    Dict_movlist = {}
    link = requests.get(flinksurl, headers=mozhdr, verify=False).text
    mlink = SoupStrainer(id="main-content")
    lsoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0
    Items = lsoup.findAll(class_='item-list tie_video')
    #xbmc.log(msg='========== Items: ' + str(Items), level=xbmc.LOGNOTICE)
    for eachItem in Items:
        asoup = eachItem.find(class_='post-content image-caption-format-1')
        #xbmc.log(msg='========== Item: ' + eachItem.prettify(), level=xbmc.LOGNOTICE)
        movPage = eachItem.find('a')['href']
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = flinks_img
        movTitle = eachItem.h2.a.text
        movTitle = clean_movtitle(movTitle)
        #xbmc.log(msg='==========Title: ' + movTitle + '\n========== Item Genre: ' + (asoup.text).encode('utf-8'), level=xbmc.LOGNOTICE)
        try:
            Rating = asoup.text
        except:
            Rating = ''
        if ('Adult' not in Rating):
            ItemNum = ItemNum+1
            Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc + ', MovTitle=' + movTitle.decode('utf8') })
        elif SETTINGS_ADULT == 'true':
            ItemNum = ItemNum+1
            Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc + ', MovTitle=' + movTitle.decode('utf8') })

    mlink = SoupStrainer(class_='pagination')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText = ''
    
    if 'pages' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'}).string.replace(',','')
        lastPage = re.findall('of (.*)', laPage)[0]
        lPage = int(lastPage)
        if (CurrentPage < lPage):
            paginationText = '(Currently in ' + laPage + ')'

    if 'tamil' in flinksurl:
        subUrl = 'flinkstamil'
    elif 'malayalam' in flinksurl:
        subUrl = 'flinksmalayalam'
    elif 'telugu' in flinksurl:
        subUrl = 'flinkstelugu'
    elif 'adult-hindi' in flinksurl:
        subUrl = 'flinkshindisc'
    elif 'hindi' in flinksurl:
        subUrl = 'flinkshindi'
    elif 'kannada' in flinksurl:
        subUrl = 'flinkskannada'
    elif 'adult' in flinksurl:
        subUrl = 'flinksadult'
    elif 'animation' in flinksurl:
        subUrl = 'flinksani'
    elif 'hollywood' in flinksurl:
        subUrl = 'flinksholly'
    elif 'bengali' in flinksurl:
        subUrl = 'flinksben'
    elif 'bhojpuri' in flinksurl:
        subUrl = 'flinksbhoj'
    elif 'biography' in flinksurl:
        subUrl = 'flinksbio'
    elif 'documentary' in flinksurl:
        subUrl = 'flinksdocu'
    elif 'gujarati' in flinksurl:
        subUrl = 'flinksguj'
    elif 'marathi' in flinksurl:
        subUrl = 'flinksmar'
    elif 'nepali' in flinksurl:
        subUrl = 'flinksnep'
    elif 'oriya' in flinksurl:
        subUrl = 'flinksori'
    elif 'punjabi' in flinksurl:
        subUrl = 'flinkspun'
    elif 'rajasthani' in flinksurl:
        subUrl = 'flinksraj'
    elif 'urdu' in flinksurl:
        subUrl = 'flinksurdu'
    elif '/?s=' in flinksurl:
        subUrl = 'flinkssearch'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_hlinks(hlinksurl):

    Dict_movlist = {}
    url=hlinksurl
    link = requests.get(url, headers=mozhdr).text
    soup = BeautifulSoup(link,'html5lib')
    lsoup = soup.find(class_='nag cf')
    ItemNum = 0
    Items = lsoup.find_all(lambda tag: tag.has_attr('id'))
    #Items = lsoup.find_all(class_='item-video')
    #xbmc.log(msg='========== Items: ' + str(Items), level=xbmc.LOGNOTICE)
    for eachItem in Items:
        movsec = eachItem.find(class_='thumb')
        try: movdet = eachItem.find(class_='entry-summary').text
        except: movdet = ''
        movPage = movsec.find('a')['href']
        imgSrc = movsec.find('img')['src']
        movTitle = (movsec.find('a')['title'])
        movTitle = clean_movtitle(movTitle)

        if ('Adult' not in movdet) and ('adult' not in hlinksurl):
            ItemNum = ItemNum+1
            Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc + ', MovTitle=' + movTitle.decode('utf8') })
        elif SETTINGS_ADULT == 'true':
            ItemNum = ItemNum+1
            Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movPage + ', imgLink=' + imgSrc + ', MovTitle=' + movTitle.decode('utf8') })

    Paginator = soup.find(class_='wp-pagenavi')
    paginationText = ''
    try:
        currPage = Paginator.find('span', { 'class':'current'})
    except:
        currPage = ''
            
    if currPage:    
        CurrentPage = int(currPage.string)
        lasPage = Paginator.find('span', { 'class':'pages'})
        lastPage = int(re.findall('of (.*)', lasPage.string)[0])
        
        if (CurrentPage < lastPage):
            paginationText = "(Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"


    if 'hindi-movies' in hlinksurl:
        subUrl = 'hlinkshindi'
    elif 'dubbed-movies' in hlinksurl:
        subUrl = 'hlinksdub'
    elif 'adult' in hlinksurl:
        subUrl = 'hlinksadult'
    elif 'documentaries' in hlinksurl:
        subUrl = 'hlinksdocu'
    elif '/?s=' in hlinksurl:
        subUrl = 'hlinkssearch'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_olangal(olangalurl):
    Dict_movlist = {}
    url=olangalurl
    link = requests.get(url, headers=mozhdr).text

    mlink = SoupStrainer(class_='paginado')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText = ''
    try:
        currPage = Paginator.find('a', { 'class':'current' })
    except:
        currPage = ''
            
    if currPage:    
        CurrentPage = int(currPage.contents[0].strip())
        lastPage = 1
        for eachPage in Paginator.findAll("a", { "class":"page larger"}):
            if "Next" not in eachPage.contents[0]:
                lastPage = int(eachPage.contents[0].strip())
        
        if (CurrentPage < lastPage):
            paginationText = "(Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"
        
    ItemNum=0
    mlink = SoupStrainer(class_='item_1 items')
    isoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)

    for eachItem in isoup.findAll(class_='item'):
        ItemNum=ItemNum+1
        imgfullLink = eachItem.find('img')['src']
        fullLink = eachItem.find('a')['href']
        movTitle = eachItem.find('img')['alt']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + fullLink + ', imgLink=' + imgfullLink.strip()+', MovTitle='+movTitle.decode('utf8')})
    if paginationText:
        #Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=olangalMovies-Recent, currPage=' + str(int(CurrentPage) + 1) + ',title=Next Page.. ' + paginationText+', Order='+str(ItemNum)})
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})
    return Dict_movlist

def getMovList_ABCmal(abcmalUrl):
    Dict_movlist = {}
    link = requests.get(abcmalUrl, headers=mozhdr).text
    base_url = 'http://abcmalayalam.com'
    mlink = SoupStrainer(class_='itemContainer')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum=0
    for linksSection in Items:
        ItemNum = ItemNum+1
        itemdet = linksSection.find(class_='catItemImage')
        movUrl = base_url + itemdet.find('a')['href']
        movName = itemdet.find('a')['title']
        imgSrc = base_url + itemdet.find('img')['src']
        
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movUrl + ', imgLink=' + imgSrc + ', MovTitle=' + movName})

    mlink = SoupStrainer(class_='k2Pagination')
    psoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ptext = re.search('(Page .*?) <', str(psoup))
    if ptext:
        paginationText = '(Currently in ' + ptext.group(1) + ')'
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(int(currPage) + 21) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_tamiltv(tamiltvurl):
    Dict_movlist = {}
    link = requests.get(tamiltvurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='pm-li-video')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum=0
    for Item in Items:
        ItemNum = ItemNum+1
        movUrl = Item.a.get('href')
        movName = Item.a.img.get('alt')
        imgSrc = Item.a.img.get('src')
        
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movUrl + ', imgLink=' + imgSrc + ', MovTitle=' + movName})

    mlink = SoupStrainer(class_='pagination pagination-centered')
    psoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    #xbmc.log(msg = 'psoup:======>\n' + psoup.prettify().encode('utf8'), level = xbmc.LOGNOTICE)
    CurrentPage = psoup.find(class_='active')
    #xbmc.log(msg = 'CurrentPage:======>\n' + CurrentPage.prettify(), level = xbmc.LOGNOTICE)
    currPage = int(CurrentPage.a.text)
    pages = psoup.find_all('a')
    lastPage = 1
    for page in pages:
        if page.text.isnumeric():
            if int(page.text) > lastPage:
                lastPage = int(page.text)

    if currPage < lastPage:
        paginationText = '(Currently in Page ' + str(currPage) + ' of ' + str(lastPage) + ' )'
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(currPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_lmtv(lmtvurl):
    Dict_movlist = {}
    link = requests.get(lmtvurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='moviefilm')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum=0
    for Item in Items:
        ItemNum = ItemNum+1
        movUrl = Item.a.get('href')
        movName = Item.img.get('alt')
        imgSrc = Item.img.get('src')
        
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movUrl + ', imgLink=' + imgSrc + ', MovTitle=' + movName})

    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'})
        lastPage = laPage.string
        lPage = int(re.findall('of (.*)', lastPage)[0])

        if (CurrentPage < lPage):
            paginationText = "(Currently in " + lastPage + ")\n"
            Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_yamgo(yamgourl):
    Dict_movlist = {}
    link = requests.get(yamgourl, headers=mozhdr).text
    token = re.findall('access_token=([^&]*)', link)[0]
    cvar = re.findall('var channels=(.*?);var channel', link)[0]
    cdata = json.loads(cvar)
    mlink = SoupStrainer(class_='epg-channel cat-Bollywood')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum=0
    for Item in Items:
        ItemNum = ItemNum+1
        yid = Item.get('id')
        cid = cdata[yid][0]['channel_id']
        movUrl = 'https://api2.yamgo.com/channel/%s?access_token=%s&os=desktopv3'%(cid, token)
        movName = cdata[yid][0]['channel_name']
        imgSrc = cdata[yid][0]['channel_images_logo_large']
        if not imgSrc:
            imgSrc = cdata[yid][0]['channel_images_tn_large']
        #xbmc.log(msg='========== movurl: ' + movUrl, level=xbmc.LOGNOTICE)
        #xbmc.log(msg='========== movName: ' + movName, level=xbmc.LOGNOTICE)
        #xbmc.log(msg='========== imgSrc: ' + imgSrc, level=xbmc.LOGNOTICE)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movUrl + ', imgLink=' + imgSrc + ', MovTitle=' + movName})

    return Dict_movlist

def getMovList_KitMovie(kmovieurl):
    Dict_movlist = {}
    link = requests.get(kmovieurl, headers=mozhdr).text
    soup = BeautifulSoup(link,'html5lib')
    ItemNum=0
    Items = soup.find_all(class_='col-sm-4 col-xs-6 item responsive-height')

    for row in Items:
        ItemNum=ItemNum+1
        img=row.find('img')['src']
        if '//' in str(img[ 0 : 0 + 2]):
            img=img.replace("//", "http://")
        currMovObj=row.find('h3')
        movTitle=currMovObj.text
        movTitle = clean_movtitle(movTitle)
        
        for currMovObj in row.findAll("a"):
            if currMovObj.has_attr('href'):                 
                movlink=currMovObj.get('href')
                Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movlink + ', imgLink=' + img + ', MovTitle=' + movTitle.decode('utf8')})
                break

    Items = soup.find_all(class_='class":"col-sm-4 col-xs-6 item')
    for row in Items:
        ItemNum=ItemNum+1
        img=row.find('img')['src']
        if '//' in str(img[ 0 : 0 + 2]):
            img=img.replace("//", "http://")
        currMovObj=row.find('h3')
        movTitle=currMovObj.text
        movTitle = clean_movtitle(movTitle)
        
        for currMovObj in row.findAll("a"):
            if currMovObj.has_attr('href'):                 
                movlink=currMovObj.get('href')
                Dict_movlist.update({ItemNum:'mode=individualmovie, url=' + movlink + ', imgLink=' + img + ', MovTitle=' + movTitle.decode('utf8')})
                break

    #Paginator = soup.find(class_='pagination')
    #mlink = SoupStrainer(class_='pagination')
    Paginator = soup.find(class_='pagination')
    paginationText = ''
    try:
        currPage = Paginator.find('span', { 'class':'page-numbers current'})
    except:
        currPage = ''
            
    if currPage:    
        CurrentPage = int(currPage.string)
        for eachPage in Paginator.findAll("a", { "class":"page-numbers"}):
            if "Next" not in eachPage.contents[0] and "Prev" not in eachPage.contents[0]:
                lastPage = int(eachPage.string)
        
        if (CurrentPage < lastPage):
            paginationText = "(Currently in Page " + str(CurrentPage) + " of " + str(lastPage) + ")\n"

    if '/hindi/' in kmovieurl:
        if '/movies/' in kmovieurl:
            subUrl = 'KitMovie_Hindi'
        elif '/songs/' in kmovieurl:
            subUrl = 'KitMovie_HSongs'
        elif '/?s=' in kmovieurl:
            subUrl = 'KitMovie_hsearch'            
    elif '/tamil/' in kmovieurl:
        if '/movie/' in kmovieurl:
            subUrl = 'KitMovie_Tamil'
        elif '/songs/' in kmovieurl:
            subUrl = 'KitMovie_TSongs'
        elif '/?s=' in kmovieurl:
            subUrl = 'KitMovie_tsearch' 
    elif '/malayalam/' in kmovieurl:
        if '/movie/' in kmovieurl:
            subUrl = 'KitMovie_Mal'
        elif '/songs/' in kmovieurl:
            subUrl = 'KitMovie_MSongs'
        elif '/?s=' in kmovieurl:
            subUrl = 'KitMovie_msearch' 

    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_i4m(i4murl):
    Dict_movlist = {}
    link = requests.get(i4murl, headers=mozhdr).text
    mlink = SoupStrainer(class_='entry clearfix')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    #soup = BeautifulSoup(link)
    #xbmc.log(msg='========== soup: ' + (soup.prettify().encode('utf-8')), level=xbmc.LOGNOTICE)
    ItemNum = 0
    #Items = soup.find_all(class_='entry clearfix')
    #xbmc.log(msg='========== Items: ' + str(Items), level=xbmc.LOGNOTICE)
    for eachItem in Items:
        ItemNum = ItemNum+1
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = i4m_img
        movdet = eachItem.find(class_='title')
        movPage = movdet.find('a')['href']
        movTitle = movdet.find('a').string
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'})
        lastPage = laPage.string

        if (CurrentPage < lastPage):
            paginationText = "(Currently in " + lastPage + ")\n"

    if '/tamil' in i4murl:
        subUrl = 'i4m_Tamil'
    elif '/telugu' in i4murl:
        subUrl = 'i4m_Telugu'
    elif '/marathi' in i4murl:
        subUrl = 'i4m_Marathi'
    elif '/punjabi' in i4murl:
        subUrl = 'i4m_Punjabi'
    elif '/dubbed' in i4murl:
        subUrl = 'i4m_Dubbed'
    elif '/hindi' in i4murl:
        subUrl = 'i4m_Hindi'
    elif '/hollywood' in i4murl:
        subUrl = 'i4m_English'
    elif '/kannada' in i4murl:
        subUrl = 'i4m_Kan'
    elif '/malayalam' in i4murl:
        subUrl = 'i4m_Mal'
    elif '/adult' in i4murl:
        subUrl = 'i4m_adult'
    elif '/bengali' in i4murl:
        subUrl = 'i4m_Bengali'
    elif '/pakistani' in i4murl:
        subUrl = 'i4m_Urdu'
    elif '/?s=' in i4murl:
        subUrl = 'i4m_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_yd(ydurl):
    Dict_movlist = {}
    link = requests.get(ydurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='latestPost-content')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0

    for eachItem in Items:
        ItemNum = ItemNum+1
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = yd_img
        movPage = eachItem.find('a')['href']
        movTitle = eachItem.find('a')['title']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='pagination pagination-numeric')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'Last' in str(Paginator):
        currPage = Paginator.find(class_='current')
        CurrentPage = int(currPage.text)
        pages = Paginator.find_all('a')
        for page in pages:    
            if 'Last' in page.text:
                lapage = page.get('href')
        lastPage = int(re.findall('page/(\d*)', lapage)[0])

        if (CurrentPage < lastPage):
            paginationText = '(Currently in Page %s of %s)\n'%(CurrentPage,lastPage)

    if '/star-plus' in ydurl:
        subUrl = 'yd_star'
    elif '/colors' in ydurl:
        subUrl = 'yd_colors'
    elif '/zee-tv' in ydurl:
        subUrl = 'yd_zee'
    elif '/sony-tv' in ydurl:
        subUrl = 'yd_sony'
    elif '/sab-tv' in ydurl:
        subUrl = 'yd_sab'
    elif '/life-ok' in ydurl:
        subUrl = 'yd_lok'
    elif '/star-jalsha' in ydurl:
        subUrl = 'yd_jalsha'
    elif '/tv/' in ydurl:
        subUrl = 'yd_and'
    elif '/star-pravah' in ydurl:
        subUrl = 'yd_pravah'
    elif '/mtv-india' in ydurl:
        subUrl = 'yd_mtv'
    elif '/bindass-tv' in ydurl:
        subUrl = 'yd_bind'
    elif '/channel-v' in ydurl:
        subUrl = 'yd_chv'
    elif '/e24' in ydurl:
        subUrl = 'yd_e24'
    elif '/promos-section' in ydurl:
        subUrl = 'yd_prom'
    elif '/?s=' in ydurl:
        subUrl = 'yd_search'
    else:
        subUrl = 'yd_main'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_tts(ttsurl):
    Dict_movlist = {}
    link = requests.get(ttsurl, headers=mozhdr).text
    mlink = SoupStrainer(class_='video')
    Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    ItemNum = 0

    for eachItem in Items:
        ItemNum = ItemNum+1
        try:
            imgSrc = eachItem.find('img')['src']
        except:
            imgSrc = tts_img
        movPage = eachItem.find('a')['href']
        movTitle = eachItem.find('img')['alt']
        movTitle = clean_movtitle(movTitle)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'Last' in str(Paginator):
        currPage = Paginator.find(class_='pages').text
        CurrentPage = int(re.findall('Page\s?(\d*)', currPage)[0])
        lastPage = int(re.findall('of\s?(\d*)', currPage)[0])

        if (CurrentPage < lastPage):
            paginationText = '(Currently in %s)\n'%(currPage)

    if '/sun-tv-serials' in ttsurl:
        subUrl = 'tts_sunss'
    elif '/sun-tv-shows' in ttsurl:
        subUrl = 'tts_sunsh'
    elif '/vijay-tv-serials' in ttsurl:
        subUrl = 'tts_vijayss'
    elif '/vijay-tv-shows' in ttsurl:
        subUrl = 'tts_vijaysh'
    elif '/zee-tamil-serials' in ttsurl:
        subUrl = 'tts_zeess'
    elif '/zee-tv-shows' in ttsurl:
        subUrl = 'tts_zeesh'
    elif '/raj-tv-serials' in ttsurl:
        subUrl = 'tts_rajss'
    elif '/raj-tv-shows' in ttsurl:
        subUrl = 'tts_rajsh'
    elif '/polimer-tv-serials' in ttsurl:
        subUrl = 'tts_polimerss'
    elif '/captain-tv-shows' in ttsurl:
        subUrl = 'tts_captainss'
    elif '/jaya-tv-programs' in ttsurl:
        subUrl = 'tts_jayass'
    elif '/kalaignar-tv-shows' in ttsurl:
        subUrl = 'tts_kalaiss'
    elif '/puthuyugam' in ttsurl:
        subUrl = 'tts_pyss'
    elif '/puthiya-thalaimurai-tv-shows' in ttsurl:
        subUrl = 'tts_ptss'
    elif '/?s=' in ttsurl:
        subUrl = 'tts_search'
    else:
        subUrl = 'tts_main'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovList_mfish(mfishurl):
    Dict_movlist = {}
    link = requests.get(mfishurl, headers=mozhdr).text
    soup = BeautifulSoup(link, 'html5lib')
    videoclass = soup.find(class_='loop-content switchable-view list-medium')
    #xbmc.log(msg='========== videoclass: ' + (videoclass.prettify().encode('utf-8')), level=xbmc.LOGNOTICE)
    ItemNum = 0
    Items = videoclass.find_all(class_='thumb')
    for eachItem in Items:
        ItemNum = ItemNum+1
        movTitle = eachItem.find('a')['title']
        movTitle = clean_movtitle(movTitle)
        movPage = eachItem.find('a')['href']
        imgSrc = eachItem.find('img')['src']
        #xbmc.log(msg='========== Item: \n title: ' + movTitle.decode('utf8') + '\n href= ' + movPage, level=xbmc.LOGNOTICE)
        Dict_movlist.update({ItemNum:'mode=individualmovie, url=%s, imgLink=%s, MovTitle=%s'%(movPage,imgSrc,movTitle.decode('utf8'))})

    mlink = SoupStrainer(class_='wp-pagenavi')
    Paginator = BeautifulSoup(link, 'html.parser', parse_only=mlink)
    paginationText=''
    
    if 'larger' in str(Paginator):
        currPage = Paginator.find('span', { 'class':'current'})
        CurrentPage = int(currPage.string)
        laPage = Paginator.find('span', { 'class':'pages'})
        lastPage = laPage.string
        lPage = int(re.findall('of (.*)', lastPage)[0])

        if (CurrentPage < lPage):
            paginationText = '(Currently in ' + lastPage + ')\n'

    if '-tamil' in mfishurl:
        subUrl = 'mfish_Tamil'
    elif '/telugu' in mfishurl:
        subUrl = 'mfish_Telugu'
    elif '-malayalam' in mfishurl:
        subUrl = 'mfish_Mal'
    elif '/punjabi' in mfishurl:
        subUrl = 'mfish_Punjabi'
    elif '/hindi-dubbed' in mfishurl:
        subUrl = 'mfish_Dubbed'
    elif '/dubbed' in mfishurl:
        subUrl = 'mfish_SDubbed'
    elif '/all-video' in mfishurl:
        subUrl = 'mfish_Hindi'
    elif '/hollywood' in mfishurl:
        subUrl = 'mfish_English'
    elif '?s=' in mfishurl:
        subUrl = 'mfish_search'
        
    if paginationText:
        Dict_movlist.update({'Paginator':'mode=GetMovies, subUrl=' + subUrl + ', currPage=' + str(CurrentPage + 1) + ',title=Next Page.. ' + paginationText + ',search_text=' + search_text})

    return Dict_movlist

def getMovLinksForEachMov(url):

    url = _DD.queries.get('url', False)
    movTitle = str(_DD.queries.get('title', False))
    fanarturl = str(_DD.queries.get('fanarturl', False))

    if 'olangal.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='entry-content')
        videoclass = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []
        
        try:
            links = videoclass.find_all('a')
            for link in links:
                vidurl = link.get('href')
                resolve_media(vidurl, sources)
        except:
            print " : no embedded urls found using method 1"

        try:
            links = videoclass.find_all('iframe')
            for link in links:
                vidurl = link.get('src')
                resolve_media(vidurl, sources)

        except:
                 print 'Nothing found using method 2!'

        try:
            mlink = SoupStrainer(class_='movieplay')
            links = BeautifulSoup(link, 'html.parser', parse_only=mlink)
            for link in links:
                try:
                    vidurl = link.find('iframe')['src']
                    resolve_media(vidurl, sources)

                except:
                    print 'Nothing found using method 3!'
        except:
                print 'Nothing found using method 3!'

        list_media(movTitle, sources, fanarturl)

    elif 'mersalaayitten.' in url:

        movid = re.findall('video/([\\d]*)',url)[0]
        xmlurl = 'http://mersalaayitten.us/media/nuevo/econfig.php?key=' + movid
        headers = {'User-Agent': mozagent,
                   'Referer': 'http://mersalaayitten.us/media/nuevo/player.swf'}
        link = requests.get(xmlurl, headers=headers).text
        soup = BeautifulSoup(link)

        try:
            movfile = soup.file.text
            thumb = soup.thumb.text
            li = xbmcgui.ListItem(movTitle, iconImage=thumb)
            li.setArt({ 'fanart': thumb })
            li.setProperty('IsPlayable', 'true')
            try:
                srtfile = soup.captions.text
                li.setSubtitles(['special://temp/mersal.srt', srtfile])
            except:
                print "No Subtitles"
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), movfile, li)
        except:
            print "Nothing found"

    elif 'tamiltvsite.' in url:

        slink = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer('div', {'id':'Playerholder'})
        soup = BeautifulSoup(slink, 'html.parser', parse_only=mlink)
        movfile=''

        try:
            tlink = soup.iframe.get('src')
            link = requests.get(tlink, headers=mozhdr).text
            strdata = re.findall('var act_data = (.*?);', link)[0]
            act_data = json.loads(strdata)
            act_url = act_data["url"]
            if '>>>>' in act_url:
                act_url = act_url.split('>>>>')[0]
            act_url = 'http://tamiltvsite.com/channels/channel.php?' + act_url.split('?')[1]
            link = requests.get(act_url, headers=mozhdr).text
            strdata = re.findall('act_data = ({.*?});', link)[0]
            act_data = json.loads(strdata)
            tlink = act_data["url"]
            
            if 'embed.' in tlink:
                movfile = tlink.split('embed')[0] + 'index.m3u8'
            
            elif 'wmsAuthSign' in tlink:
                new_token = re.findall('new_token = "(.*?)"', link)[0]
                movfile = tlink.split('?')[0] + '?wmsAuthSign=' + new_token
                    
            elif ('dacast.' in tlink) or ('streamingasaservice.' in tlink):
                surl = tlink.split('.com')[1]
                dheaders = {'User-Agent': mozagent,
                           'Referer': 'http://iframe.dacast.com/'}
                link = requests.get('http://json.dacast.com' + surl, headers=dheaders).text
                act_data = json.loads(link)
                act_url = act_data["hls"]
                link = requests.get('https://services.dacast.com/token/i%s?'%surl, headers=dheaders, verify=False).text
                act_data = json.loads(link)
                new_token = act_data["token"]
                movfile = act_url + new_token
                
            elif 'youtube.' in tlink:
                sources = []
                resolve_media(tlink, sources)
                list_media(movTitle, sources, fanarturl)
                
            elif '.m3u8' in tlink or 'rtmp:' in tlink:
                movfile = tlink
                
            else:
                xbmc.log(msg = tlink + ' not resolvable.\n', level = xbmc.LOGNOTICE)
        except:
            print "no embedded urls found using iframe method"

        if movfile:
            li = xbmcgui.ListItem(movTitle)
            li.setArt({ 'thumb': fanarturl })
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), movfile, li)

    elif 'tamilyogi.' in url:

        link = requests.get(url, headers=mozhdr).text
        #mlink = SoupStrainer(class_='entry')
        #soup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        soup = BeautifulSoup(link, 'html5lib')
        lsoup = soup.find(class_='entry')
        links = lsoup.find_all('iframe')
        sources = []

        for link in links:
            try:
                vidurl = link.get('src')
                resolve_media(vidurl, sources)
            
            except:
                print 'Nothing found using iframe method!'

        list_media(movTitle, sources, fanarturl)

    elif 'yamgo.' in url:
        headers = {'Referer' : 'http://yamgo.com/',
                  'User-Agent': mozagent,
                  'Origin' : 'http://yamgo.com'}
        val = requests.get(url, headers=headers, verify=False).text
        jdata=json.loads(val)
        movfile=''

        try:
            tlink = jdata['data']['channel_stream']
            if 'yamgo.' in tlink:
                movfile = tlink
               
        except:
            print "no embedded urls found using yamgo method"

        if movfile:
            li = xbmcgui.ListItem(movTitle)
            li.setArt({ 'thumb': fanarturl })
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), movfile, li)

    elif 'livemalayalamtv.' in url:

        slink = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='filmicerik')
        soup = BeautifulSoup(slink, 'html.parser', parse_only=mlink)
        movfile=''

        try:
            tlink = soup.iframe.get('src')
            if 'livemalayalamtv.' in tlink:
                link = requests.get(tlink, headers=mozhdr).text
                if 'unescape(' in link:
                    strdata = re.findall("unescape\('(.*?)'", link)[0]
                    link = urllib.unquote(strdata)
                movfile = re.findall('stream = "(.*?)"',link)[0] #+ '|User-Agent=' + mozagent
               
            else:
                xbmc.log(msg = tlink + ' not resolvable.\n', level = xbmc.LOGNOTICE)
        except:
            print "no embedded urls found using iframe method"
            
        if movfile:
            li = xbmcgui.ListItem(movTitle)
            li.setArt({ 'thumb': fanarturl })
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), movfile, li)

    elif 'rajtamil.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='entry-content')
        videoclass = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        #xbmc.log(msg='========== Videoclass: ' + (videoclass.prettify().encode('utf-8')), level=xbmc.LOGNOTICE)
        sources = []
            
        try:
            links = videoclass.find_all('iframe')
            for plink in links:
                movLink = plink.get('src')
                resolve_media(movLink, sources)

        except:
            print "no embedded urls found using iframe method"

        try:
            links = videoclass.find_all('a')
            #xbmc.log(msg = '============== links: ' + str(links), level = xbmc.LOGNOTICE)
            for alink in links:
                movLink = alink.get('href')
                resolve_media(movLink, sources)

        except:
            print "no embedded urls found using a method"
            
        try:
            links = videoclass.find_all('embed')
            for elink in links:
                movLink = elink.get('src')
                resolve_media(movLink, sources)
        except:
            print "no embedded urls found using embed method"

        try:           
            movLink = re.findall("[\d\D]+window.open\('([^']*)", str(videoclass))[0]
            resolve_media(movLink, sources)
        except:
            print "no embedded urls found using open method"

        list_media(movTitle, sources, fanarturl)

    elif 'redmovies.' in url:

        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link,'html5lib')
        #lsoup = soup.find(class_='entry-content rich-content')
        lsoup = soup.find(id="content")
        #xbmc.log(msg='========== lsoup: \n' + (lsoup.prettify().encode('utf-8')), level=xbmc.LOGNOTICE)
        sources = []
                    
        try:
            links = lsoup.find_all('div', { 'class':'tabs-catch-all' })
            for plink in links:
                movLink = plink.find('iframe')[('src')]
                resolve_media(movLink, sources)

        except:
            print 'no embedded urls found using tabs method'
                   
        try:
            tlink = soup.find(class_='table')
            #xbmc.log(msg='========== soup: ' + (tlink.prettify().encode('utf-8')), level=xbmc.LOGNOTICE)
            links = tlink.find_all('a')
            #xbmc.log(msg='========== table links: ' + str(links), level=xbmc.LOGNOTICE)
            for plink in links:
                movLink = plink.get('href')
                resolve_media(movLink, sources)

        except:
            print 'no embedded urls found using table method'

        try:
            movLink = re.findall('<iframe.*?src="(.*?)"', lsoup.prettify())[0]
            resolve_media(movLink, sources)

        except:
            print 'no embedded urls found using regex method'
            
        list_media(movTitle, sources, fanarturl)

    elif 'cinebix.com' in url:

        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link)
        sources = []
        
        try:
            links = soup.find_all('iframe')
            for plink in links:
                movLink = plink.get('src')
                resolve_media(movLink, sources)

        except:
            print " : no embedded urls found using wrapper method"
            
        list_media(movTitle, sources, fanarturl)

    elif 'youtube.com' in url:

        sources = []

        try:
            resolve_media(url, sources)

        except:
            print " : no embedded urls found using wrapper method"
            
        list_media(movTitle, sources, fanarturl)    

    elif 'tamilgun.' in url:

        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link, 'html5lib')
        videoclass = soup.find(class_='videoWrapper player')     
        sources = []
        
        try:
            links = videoclass.find_all('iframe')
            for plink in links:
                movLink = plink.get('src')
                resolve_media(movLink, sources)

        except:
            print " : no embedded urls found using wrapper method"

        videoclass = soup.find(class_='post-entry')
        try:
            plinks = videoclass.find_all('p')
            for plink in plinks:
                try:
                    movLink = plink.iframe.get('src')
                    resolve_media(movLink, sources)

                except:
                    print " : no embedded urls found using postentry method"

        except:
            print " : no embedded urls found using post entry iframe method"

        try:
            plinks = videoclass.find_all('a')
            for plink in plinks:
                try:
                    movLink = plink.get('href')
                    resolve_media(movLink, sources)
                        
                except:
                    print " : no embedded urls found using postentry method"
                            
        except:
            print " : no embedded urls found using post entry a method"

        try:
            jlink = re.findall('sources:.*file":"([^"]*)', link)[0]
            elink = jlink.replace('\\/', '/')
            if ('tamilgun' in elink) or ('m3u8' in elink):
                li = xbmcgui.ListItem('tamilgun.us', iconImage=fanarturl)
                li.setArt({ 'fanart': fanarturl })
                li.setProperty('IsPlayable', 'true')
                elink += '|Referer=http://tamilgun.us'
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), elink, li)
            else:
                print '    not resolvable by urlresolver!'

        except:
            print " : no embedded urls found using embed method"
        
        list_media(movTitle, sources, fanarturl)

    elif 'filmlinks4u.' in url:

        link = requests.get(url, headers=mozhdr, verify=False).text
        mlink = SoupStrainer(class_='post-single-content box mark-links')
        lsoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []
        itemdetails = lsoup.findAll('p')
        #xbmc.log(msg='========== Itemdet: ' + str(itemdetails), level=xbmc.LOGNOTICE)
        cleanmov = True
        for eachdetail in itemdetails:
            if 'Adult' in str(eachdetail):
                cleanmov = False
        #xbmc.log(msg='==========cleanmov: ' + str(cleanmov) + ' adult setting:' + SETTINGS_ADULT, level=xbmc.LOGNOTICE)
        
        try:
            ilink = lsoup.find("iframe")
            vidurl = ilink.get('src')
            #xbmc.log(msg='========== vidurl: ' + vidurl, level=xbmc.LOGNOTICE)
            if cleanmov:
                resolve_media(vidurl, sources)
            elif SETTINGS_ADULT == 'true':
                resolve_media(vidurl, sources)

        except:
            print " : no embedded urls found using iframe method"
            
        try:
            blink = re.findall("ajaxurl = '(.*?)'", link)[0]
            postid = re.findall("'post_id':'(.*?)'", link)[0]
            values = {'action' : 'create_player_box',
                      'post_id' : postid }
            headers = {'Referer' : 'https://www.filmlinks4u.is/',
                      'User-Agent': mozagent,
                      'X-Requested-With' : 'XMLHttpRequest'}
            playbox = requests.post(blink, data=values, headers=headers, verify=False).text
            mlink2 = SoupStrainer(class_='tabs')
            tsoup = BeautifulSoup(playbox, 'html.parser', parse_only=mlink2)
            tabs = tsoup.find_all(class_='tab')
            #xbmc.log(msg='========== Tabs: ' + str(tabs), level=xbmc.LOGNOTICE)
            for eachtab in tabs:
                if eachtab.has_attr('data-href'):
                    vidurl = eachtab.get('data-href')
                else:
                    vidurl = eachtab.find('a')['href']
                #xbmc.log(msg='========== vidurl: ' + vidurl, level=xbmc.LOGNOTICE)
                if cleanmov:
                    resolve_media(vidurl, sources)
                elif SETTINGS_ADULT == 'true':
                    resolve_media(vidurl, sources)

        except:
            print " : no embedded urls found using player_box method"
            
        try:
            links = lsoup.findAll(class_='external')
            for plink in links:
                vidurl = re.findall('href="(.*?)"', str(plink))[0]
                if cleanmov:
                    resolve_media(vidurl, sources)
                elif SETTINGS_ADULT == 'true':
                    resolve_media(vidurl, sources)
                
        except:
            print " : no embedded urls found using cineview method"


        try:
            mlink = SoupStrainer(class_='entry')
            lsoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)            
            links = lsoup.findAll('p')
            for plink in links:
                try:
                    vidurl = plink.a.get('href')
                    if cleanmov:
                        resolve_media(vidurl, sources)
                    elif SETTINGS_ADULT == 'true':
                        resolve_media(vidurl, sources)
                except:
                    print " : no embedded urls found using a method"
        except:
            print " : no embedded urls found using p-a method"
            
        list_media(movTitle, sources, fanarturl)

    elif 'hindilinks4u.' in url:

        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link, 'html5lib')
        sources = []

        try:
            linksDiv = soup.find(class_='screen fluid-width-video-wrapper')
            try:
                vidurl = str(linksDiv.find('iframe')['src'])
                resolve_media(vidurl, sources)
            except:
                print 'Nothing found using method 1!'
            try:
                vidtab = (re.findall('prepend\( "(.*?)" \)', str(linksDiv))[0]).replace('\\', '')
                vsoup = BeautifulSoup(vidtab)
                #xbmc.log(msg='==== vsoup: \n' + (vsoup.prettify().encode('utf-8')), level=xbmc.LOGNOTICE)
                vtabs = vsoup.find_all('span')
                #vtabs = vsoup.find_all(lambda tag: tag.name == 'span' and 'src' in tag.attrs)
                #xbmc.log(msg='==== vtabs: \n' + str(vtabs), level=xbmc.LOGNOTICE)
                for vtab in vtabs:
                    vidurl = vtab['data-href']
                    resolve_media(vidurl, sources)
            except:
                print 'Nothing found using method 1!'
        except:
            print 'Nothing found using method 1!'

        try:
            linksDiv = soup.find(class_='entry-content rich-content')
            links = linksDiv.find_all('a')
            for link in links:
                vidurl = link.get('href').strip()
                resolve_media(vidurl, sources)
        except:
            print 'Nothing found using method 2!'

        list_media(movTitle, sources, fanarturl)

    elif 'movierulz.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='entry-content')
        soup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []
        links = soup.find_all('a')
        #xbmc.log(msg='========== links: ' + str(links), level=xbmc.LOGNOTICE)
        for link in links:
            try:
                vidurl = link.get('href')
                resolve_media(vidurl, sources)
            except:
                print 'Nothing found using method 1!'
                
        list_media(movTitle, sources, fanarturl)

    elif 'moviefk.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='entry-content clearfix')
        soup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        links = soup.find_all('p')
        sources = []

        for link in links:
            try:
                vidurl = link.a['href']
                resolve_media(vidurl, sources)
            
            except:
                print 'Nothing found using method 1!'

        list_media(movTitle, sources, fanarturl)

    elif 'runtamil.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='video-content')
        soup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []
        
        plinks = soup.find_all('p')
        for plink in plinks:
            #xbmc.log(msg='========== plink: ' + plink.prettify().encode('utf-8'), level=xbmc.LOGNOTICE)
            try:
                links = plink.find_all('iframe')
                for link in links:
                    vidurl = link.get('src')
                    if ('runtamil' in vidurl) and ('facebook' not in vidurl):
                        headers = {'Referer' : url,
                                  'User-Agent': mozagent}
                        slink = requests.get(vidurl, headers=headers).text
                        hoster = 'RunTamil '
                        srclist = re.search('(\[.*?\])', slink).group(1).replace('file', '"file"').replace('label', '"label"')
                        strlinks = eval(srclist)
                        for strlink in strlinks:
                            #xbmc.log(msg='========== link: ' + str(strlink), level=xbmc.LOGNOTICE)
                            elink = strlink['file']
                            qual = ''
                            if 'label' in strlink:
                                qual = strlink['label']
                            else:
                                qual = 'HLS'
                            li = xbmcgui.ListItem(hoster + qual)
                            li.setArt({ 'fanart': fanarturl })
                            li.setProperty('IsPlayable', 'true')
                            xbmcplugin.addDirectoryItem(int(sys.argv[1]), elink, li)
                    else:
                        resolve_media(vidurl, sources)
                
            except:
                print 'Nothing found using method 1!'

            # try:
                # tlink = plink.text.encode('ascii','ignore')
                # xbmc.log(msg='========== tlink: ' + tlink, level=xbmc.LOGNOTICE)
                # vidurl = re.search('mp4=([^=]*)', tlink)
                # if vidurl:
                    # resolve_media(vidurl.group(1), sources)
                
            # except:
                # print 'Nothing found using method 2!'

        list_media(movTitle, sources, fanarturl)

    elif 'thiruttuvcd.' in url:

        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link)
        sources = []

        try:
            linksDiv = soup.find("div", { "class":"textsection col-lg-4 col-xs-12" })
            links = linksDiv.find_all('a')			
            for link in links:
                vidurl = link.get('href').strip()
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using method 1!'

        try:
            links = soup.find_all('iframe')
            for link in links:
                vidurl = link.get("data-lazy-src")
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using method 2!'

        try:
            linksDiv = soup.find(class_='videosection')
            links = linksDiv.find_all('iframe')
            for link in links:
                vidurl = link.get("src")
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using method 3!'

        list_media(movTitle, sources, fanarturl)

    elif 'thiruttuvcds.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='videosection')
        linksDiv = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []

        try:
            links = linksDiv.find_all('iframe')			
            for link in links:
                vidurl = link.get('src').strip()
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using iframe method!'

        list_media(movTitle, sources, fanarturl)

    elif 'thiruttumasala.' in url:

        headers = {'User-Agent': mozagent,
                   'Accept-Encoding': 'deflate'}
        link = requests.get(url, headers=headers).text
        soup = BeautifulSoup(link)
        #print soup.prettify()
        try:
            re1='.*?'    # Non-greedy match on filler
            re2='(var)'    # Word 1
            re3='(\\s+)'    # White Space 1
            re4='(cnf)'    # Word 2
            re5='(=)'    # Any Single Character 1
            re6='(.)'    # Any Single Character 2
            re7='(http)'    # Word 3
            re8='(:)'    # Any Single Character 3
            re9='(\\/)'    # Any Single Character 4
            re10='(\\/www\\.thiruttumasala\\.com\\/media\\/nuevo\\/config\\.php)'    # Unix Path 1
            re11='(.)'    # Any Single Character 5
            re12='(key)'    # Word 4
            re13='(=)'    # Any Single Character 6
            re14='(\\d+)'    # Integer Number 1

            rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11+re12+re13+re14,re.IGNORECASE|re.DOTALL)
            m = rg.search(str(soup))
            if m:
                word1=m.group(1)
                ws1=m.group(2)
                word2=m.group(3)
                c1=m.group(4)
                c2=m.group(5)
                word3=m.group(6)
                c3=m.group(7)
                c4=m.group(8)
                unixpath1=m.group(9)
                c5=m.group(10)
                word4=m.group(11)
                c6=m.group(12)
                int1=m.group(13)
                link= word3+c3+c4+unixpath1+c5+word4+c6+int1
                link=link.replace('config.php', 'playlist.php')
                #print 'BLAAA found link =' + link

                link = requests.get(link, headers=mozhdr).text
                soup = BeautifulSoup(link)

                li = xbmcgui.ListItem(movTitle, iconImage=soup.find('thumb').text.strip())
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), soup.find('file').text, li)

        except:
            print "Nothing found with method 1"

        try:
            txt = soup.find('param', {'name':'flashvars'})['value']
            re1 = '.*?'  # Non-greedy match on filler
            re2 = '((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'  # HTTP URL 1

            rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
            m = rg.search(txt)
            if m:
                httpurl1 = m.group(1)
                # #print "("+httpurl1+")"+"\n"
                httpurl1 = httpurl1.replace('config.php', 'playlist.php')
                link = requests.get(httpurl1, headers=mozhdr).text
                soup = BeautifulSoup(link)
                li = xbmcgui.ListItem(movTitle, iconImage=soup.find('thumb').text.strip())
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), soup.find('file').text, li)
        except:
            print "Nothing found using method 2"

    elif 'abcmalayalam.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer(class_='itemFullText')
        linksDiv = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []

        try:
            for linksSection in linksDiv.findAll(class_='avPlayerWrapper avVideo'):
                vidurl = str(linksSection.find('iframe')['src'])
                if 'http:' not in vidurl:
                    vidurl = 'http:' + vidurl
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using method 1!'

        try:
            table = linksDiv.find('table')
            links = table.find_all('a')
            for link in links:
                vidurl = link.get('href').strip()
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using method 2!'

        try:
            mlink = SoupStrainer(class_='itemIntroText')
            linksDiv = BeautifulSoup(link, 'html.parser', parse_only=mlink)
            for linksSection in linksDiv.findAll(class_='avPlayerWrapper avVideo'):
                vidurl = str(linksSection.find('iframe')['src'])
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using method 3!'

        list_media(movTitle, sources, fanarturl)

    elif 'kitmovie.' in url:
       
        sources = []
        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link, 'html5lib')
        
        try:
            linksDiv = soup.find_all(class_='pagination post-tape')
            for div in linksDiv:
                links = div.findAll('a')
                for a in links:
                    slink = requests.get(a['href'], headers=mozhdr).text
                    try:
                        mlink = SoupStrainer(class_='player player-small embed-responsive embed-responsive-16by9')
                        linksSection = BeautifulSoup(slink, 'html.parser', parse_only=mlink)
                        vidurl = str(linksSection.find('iframe')['src'])
                        resolve_media(vidurl, sources)           
                    except:
                        print 'Nothing found on tape page!'
        except:
            print 'Nothing found using tape method!'
            
        try:
            linksSection = soup.find(class_='player player-small embed-responsive embed-responsive-16by9')
            vidurl = str(linksSection.find('iframe')['src'])
            resolve_media(vidurl, sources)
        except:
            print 'Nothing found using iframe method!'            
                
        list_media(movTitle, sources, fanarturl)

    elif 'tamiltwists.' in url:

        link = requests.get(url, headers=mozhdr).text
        sources = []

        try:
            mlink = SoupStrainer(class_='video-embed')
            linksDiv = BeautifulSoup(link, 'html.parser', parse_only=mlink)
            links = linksDiv.find_all('iframe')			
            for link in links:
                vidurl = link.get('src')
                resolve_media(vidurl, sources)
        except:
                 print 'Nothing found using entry-title method!'

        list_media(movTitle, sources, fanarturl)

    elif 'india4movie.' in url:

        link = requests.get(url, headers=mozhdr).text
        mlink = SoupStrainer('p')
        soup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
        sources = []

        for link in soup:
            try:
                vidurl = link.a['href']
                resolve_media(vidurl, sources)
            
            except:
                print 'Nothing found using method 1!'

        list_media(movTitle, sources, fanarturl)

    elif 'yodesi.' in url:

        link = requests.get(url, headers=mozhdr).text
        sources = []
        try:
            mlink = SoupStrainer('iframe')
            Items = BeautifulSoup(link, 'html.parser', parse_only=mlink)
            #xbmc.log(msg='========== Items: ' + str(Items), level=xbmc.LOGNOTICE)
            for Item in Items:
                vidurl = Item.get('src')
                resolve_media(vidurl, sources)
            
        except:
            print 'Nothing found using iframe method!'

        try:
            mlink = SoupStrainer(class_='thecontent')
            psoup = BeautifulSoup(link, 'html.parser', parse_only=mlink)
            Items = psoup.find_all('a')
            #xbmc.log(msg='========== Items: ' + str(Items), level=xbmc.LOGNOTICE)
            for Item in Items:
                vidurl = Item.get('href')
                if 'yodesi.net/player.php' in vidurl:
                    vidurl = vidurl.replace('yodesi.net','yo-desi.com')
                resolve_media(vidurl, sources)
            
        except:
            print 'Nothing found using embed method!'
            
        list_media(movTitle, sources, fanarturl)

    elif 'tamiltvshows.' in url:

        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link, 'html5lib')
        psoup = soup.find(class_='entry')
        sources = []
        try:
            Items = psoup.find_all('iframe')
            for Item in Items:
                vidurl = Item.get('src')
                if 'http' in vidurl:
                    resolve_media(vidurl, sources)
            
        except:
            print 'Nothing found using iframe method!'

        try:
            Items = psoup.find_all('a')
            for Item in Items:
                if 'onclick' in str(Item):
                    clkurl = Item.get('onclick')
                    vidurl = re.findall("'(http.*?)'", clkurl)[0]
                    resolve_media(vidurl, sources)
            
        except:
            print 'Nothing found using click method!'
            
        list_media(movTitle, sources, fanarturl)

    elif 'moviefisher' in url:
        
        link = requests.get(url, headers=mozhdr).text
        soup = BeautifulSoup(link, 'html5lib')
        lsoup = soup.find(class_='entry-content rich-content')
        Items = lsoup.find_all('iframe')
        sources = []
        for eachItem in Items:
            try:
                vidurl = eachItem.get('src')
                resolve_media(vidurl, sources)
            
            except:
                print 'Nothing found using method 1!'

        list_media(movTitle, sources, fanarturl)
        
CurrUrl=str(_DD.queries.get('url', False))


if play:

    url = _DD.queries.get('url', '')
    if 'google.' in url:
        stream_url = url
    else:
        stream_url = resolve_url(url)
    if stream_url:
        _DD.resolve_url(stream_url)

elif mode == 'individualmovie':
    url = _DD.queries.get('url', False)
    getMovLinksForEachMov(url)

elif mode == 'GetMovies':
    dlg = xbmcgui.DialogProgress()
    dlg.create("Deccan Delight", "Fetching movies and caching...\nWill be faster next time")
    dlg.update(0)
    subUrl = _DD.queries.get('subUrl', False)
    mode = _DD.queries.get('mode', False)
    Url = _DD.queries.get('Url', False)
    currPage = _DD.queries.get('currPage', False)
    if not currPage:
        currPage = 1
    search_text = _DD.queries.get('search_text', False)
    if not search_text:
        search_text = ''
        
    if 'ABCMalayalam' in subUrl:
        currPage = _DD.queries.get('currPage', False)
        if not currPage:
            currPage = 0

        if subUrl == 'ABCMalayalam-Mal':
            abcmalUrl = 'http://abcmalayalam.com/movies?start=%s'%(currPage)
        elif subUrl == 'ABCMalayalam-shortFilm':
            abcmalUrl = 'http://abcmalayalam.com/short-film?start=%s'%(currPage)

        Dict_res = cache.cacheFunction(getMovList_ABCmal, abcmalUrl)

    elif 'olangal' in subUrl:

        if 'olangalMovies' in subUrl:
            olangalurl = 'http://olangal.pro/page/%s'%(currPage)
        elif 'olangalsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Olangal')
                search_text = search_text.replace(' ', '+')
            olangalurl = 'http://olangal.pro/page/%s/?s=%s'%(currPage,search_text)

        Dict_res = cache.cacheFunction(getMovList_olangal, olangalurl)

    elif 'lmtv' in subUrl:

        lmtvurl = 'http://www.livemalayalamtv.com/page/%s'%(currPage)
        Dict_res = cache.cacheFunction(getMovList_lmtv, lmtvurl)

    elif 'yamgo' in subUrl:

        yamgourl = 'http://yamgo.com/'
        Dict_res = cache.cacheFunction(getMovList_yamgo, yamgourl)

    elif 'thiruttuvcd' in subUrl:

        if 'thiruttuvcd_masala' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttumasala.com/videos?o=mr&page=%s'%(currPage)
        elif 'thiruttuvcd_MalayalamMovs' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/category/malayalam/page/%s/'%(currPage)     
        elif 'thiruttuvcd_adult' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/category/hot-movies/page/%s/'%(currPage)
        elif 'thiruttuvcd_tamilMovs' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/category/tamil-movies-online/page/%s/'%(currPage)
        elif 'thiruttuvcd_teluguMovs' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/category/watch-telugu-movie/page/%s/'%(currPage)
        elif 'thiruttuvcd_hindiMovs' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/category/hindi-movies-online/page/%s/'%(currPage)
        elif 'thiruttuvcd_tamiltv' in subUrl:
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/tv/page/%s/'%(currPage)
        elif 'thiruttuvcd_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('ThiruttuVCD')
                search_text = search_text.replace(' ', '+')
            thiruttuvcd_url = 'http://www.thiruttuvcd.me/page/%s/?s=%s'%(currPage,search_text)
        elif 'thiruttuvcd_msearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Thiruttu Masala')
                search_text = search_text.replace(' ', '+')
            thiruttuvcd_url = 'http://www.thiruttumasala.com/search?search_query=%s&search_type=videos&page=%s'%(search_text,currPage)

        #cache.delete("%")
        Dict_res = cache.cacheFunction(getMovList_thiruttuvcd, thiruttuvcd_url)

    elif 'tvcds' in subUrl:

        if 'tvcds_english' in subUrl:
            tvcds_url = 'http://thiruttuvcds.com/my/category/english/page/%s/'%(currPage)
        elif 'tvcds_adult' in subUrl:
            tvcds_url = 'http://thiruttuvcds.com/private/?paged=%s'%(currPage)
        elif 'tvcds_tamil' in subUrl:
            tvcds_url = 'http://thiruttuvcds.com/my/category/new-tamil-movies/page/%s/'%(currPage)
        elif 'tvcds_telugu' in subUrl:
            tvcds_url = 'http://thiruttuvcds.com/my/category/telugu/page/%s/'%(currPage)
        elif 'tvcds_hindi' in subUrl:
            tvcds_url = 'http://thiruttuvcds.com/my/category/hindi/page/%s/'%(currPage)
        elif 'tvcds_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Thiruttu VCDs')
                search_text = search_text.replace(' ', '+')
            tvcds_url = 'http://thiruttuvcds.com/my/page/%s/?s=%s'%(currPage,search_text)

        #cache.delete("%")
        Dict_res = cache.cacheFunction(getMovList_tvcds, tvcds_url)

    elif 'rajtamil' in subUrl:
            
        if 'rajtamildubbed' in subUrl:
            rajTamilurl = 'http://www.rajtamil.com/category/tamil-dubbed/page/%s/'%(currPage)
        elif 'rajtamilcomedy' in subUrl:
            rajTamilurl = 'http://www.rajtamil.com/category/comedy/page/%s/'%(currPage)
        elif 'rajtamilsongs' in subUrl:
            rajTamilurl = 'http://www.rajtamil.com/category/download-songs/page/%s/'%(currPage)
        elif 'rajtamilTVshowsVijayTV' in subUrl:
            rajTamilurl = 'http://www.rajtamil.com/category/vijay-tv-shows/page/%s/'%(currPage)
        elif 'rajtamilTVshowsSunTV' in subUrl:
            rajTamilurl = 'http://www.rajtamil.com/category/sun-tv-show/page/%s/'%(currPage)
        elif 'rajtamilsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('RajTamil')
                search_text = search_text.replace(' ', '+')
            rajTamilurl = 'http://www.rajtamil.com/page/%s/?s=%s'%(currPage,search_text)
        else:
            rajTamilurl = 'http://www.rajtamil.com/category/movies/page/%s/'%(currPage)

        Dict_res = cache.cacheFunction(getMovList_rajtamil, rajTamilurl)

    elif 'tamilgun' in subUrl:

        if 'tamilgunnew' in subUrl:
            tamilgunurl = 'http://tamilgun.us/categories/new-movies/page/%s/?order=latest'%(currPage)
        elif 'tamilgundubbed' in subUrl:
            tamilgunurl = 'http://tamilgun.us/categories/dubbed-movies/page/%s/?order=latest'%(currPage)
        elif 'tamilgunhd' in subUrl:
            tamilgunurl = 'http://tamilgun.us/categories/hd-movies/page/%s/?order=latest'%(currPage)
        elif 'tamilguncomedy' in subUrl:
            tamilgunurl = 'http://tamilgun.us/categories/hd-comedys/page/%s/?order=latest'%(currPage)
        elif 'tamilguntrailer' in subUrl:
            tamilgunurl = 'http://tamilgun.us/categories/trailers/page/%s/?order=latest'%(currPage)
        elif 'tamilgunsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('TamilGun')
                search_text = search_text.replace(' ', '+')
            tamilgunurl = 'http://tamilgun.us/page/%s/?s=%s'%(currPage,search_text)

        Dict_res = cache.cacheFunction(getMovList_tamilgun, tamilgunurl)

    elif 'tyogi' in subUrl:

        if 'new' in subUrl:
            tyogiurl = 'http://tamilyogi.cc/category/tamilyogi-full-movie-online/page/%s/'%(currPage)
        elif 'dubbed' in subUrl:
            tyogiurl = 'http://tamilyogi.cc/category/tamilyogi-dubbed-movies-online/page/%s/'%(currPage)
        elif 'hd' in subUrl:
            tyogiurl = 'http://tamilyogi.cc/category/tamilyogi-bluray-movies/page/%s/'%(currPage)
        elif 'dvd' in subUrl:
            tyogiurl = 'http://tamilyogi.cc/category/tamilyogi-dvdrip-movies/page/%s/'%(currPage)
        elif 'songs' in subUrl:
            tyogi_url = 'http://tamilyogi.cc/tamil-hd-movies-tamilyogi/page/%s/'%(currPage)
        elif 'trailer' in subUrl:
            tyogi_url = 'http://tamilyogi.cc/tamil-new-movies-tamilyogi/page/%s/'%(currPage)
        elif 'search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Search Tamil Yogi')
                search_text = search_text.replace(' ', '+')
            tyogi_url = 'http://tamilyogi.cc/page/%s/?s=%s'%(currPage, search_text)

        Dict_res = cache.cacheFunction(getMovList_tyogi, tyogiurl)

    elif 'runtamil' in subUrl:

        if 'runtamilnew' in subUrl:
            runtamilurl = 'http://runtamil.me/category/runtamil-new-tamil-movies2/page/%s/'%(currPage)
        elif 'runtamildubbed' in subUrl:
            runtamilurl = 'http://runtamil.me/category/runtamil-tamil-dubbed-movies/page/%s/'%(currPage)
        elif 'runtamilhd' in subUrl:
            runtamilurl = 'http://runtamil.me/category/tamil-hd-movies-online/page/%s/'%(currPage)
        elif 'runtamilold' in subUrl:
            runtamilurl = 'http://runtamil.me/category/mid-movies/old-tamil-movies/page/%s/'%(currPage)
        elif 'runtamildvd' in subUrl:
            runtamilurl = 'http://runtamil.me/category/tamil-dvd-movies1/page/%s/'%(currPage)
        elif 'runtamilsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('runtamil')
                search_text = search_text.replace(' ', '+')
            runtamilurl = 'http://runtamil.me/page/%s/?s=%s'%(currPage,search_text)

        Dict_res = cache.cacheFunction(getMovList_runtamil, runtamilurl)

    elif 'ttwist' in subUrl:

        if 'ttwistnew' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/new-movies/page/%s/?order=latest'%(currPage)
        elif 'ttwistdubbed' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/dubbed-movies/page/%s/?order=latest'%(currPage)
        elif 'ttwisthd' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/hd-movies/page/%s/?order=latest'%(currPage)
        elif 'ttwistmal' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/malayalam-movies/page/%s/?order=latest'%(currPage)
        elif 'ttwisttel' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/telugu-movies/page/%s/?order=latest'%(currPage)
        elif 'ttwisthin' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/hindi-movies/page/%s/?order=latest'%(currPage)
        elif 'ttwistadult' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/hot-masala/page/%s/?order=latest'%(currPage)
        elif 'ttwisttrailer' in subUrl:
            ttwisturl = 'http://www.tamiltwists.com/category/trailers/page/%s/?order=latest'%(currPage)
        elif 'ttwistsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Tamil Twist')
                search_text = search_text.replace(' ', '+')
            ttwisturl = 'http://www.tamiltwists.com/page/%s/?s=%s'%(currPage,search_text)

        Dict_res = cache.cacheFunction(getMovList_ttwist, ttwisturl)

    elif 'flinks' in subUrl:

        if 'flinkstamil' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/tamil/page/%s?orderby=date'%(currPage)
        elif 'flinksmalayalam' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/malayalam/page/%s?orderby=date'%(currPage)
        elif 'flinkstelugu' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/telugu/page/%s?orderby=date'%(currPage)
        elif 'flinkshindisc' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/adult-hindi-short-films/page/%s?orderby=date'%(currPage)
        elif 'flinkshindi' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/hindi/page/%s?orderby=date'%(currPage)
        elif 'flinkskannada' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/kannada/page/%s?orderby=date'%(currPage)
        elif 'flinksadult' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/adult/page/%s?orderby=date'%(currPage)
        elif 'flinksani' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/animation/page/%s?orderby=date'%(currPage)
        elif 'flinksholly' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/hollywood/page/%s?orderby=date'%(currPage)
        elif 'flinksben' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/bengali/page/%s?orderby=date'%(currPage)
        elif 'flinksbhoj' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/bhojpuri/page/%s?orderby=date'%(currPage)
        elif 'flinksbio' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/biography/page/%s?orderby=date'%(currPage)
        elif 'flinksdocu' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/documentary/page/%s?orderby=date'%(currPage)
        elif 'flinksguj' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/gujarati/page/%s?orderby=date'%(currPage)
        elif 'flinksmar' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/marathi/page/%s?orderby=date'%(currPage)
        elif 'flinksnep' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/others/nepali/page/%s?orderby=date'%(currPage)
        elif 'flinksori' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/others/oriya/page/%s?orderby=date'%(currPage)
        elif 'flinkspun' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/punjabi/page/%s?orderby=date'%(currPage)
        elif 'flinksraj' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/others/rajasthani/page/%s?orderby=date'%(currPage)
        elif 'flinksurdu' in subUrl:
            flinksurl = 'https://www.filmlinks4u.is/category/others/urdu/page/%s?orderby=date'%(currPage)
        elif 'flinkssearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('FilmLinks4U')
                search_text = search_text.replace(' ', '+')
            flinksurl = 'https://www.filmlinks4u.is/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_flinks, flinksurl)

    elif 'hlinks' in subUrl:
   
        if 'hlinkshindi' in subUrl:
            hlinksurl = 'http://www.hindilinks4u.to/category/hindi-movies/page/%s?orderby=date'%(currPage)
        elif 'hlinksdub' in subUrl:
            hlinksurl = 'http://www.hindilinks4u.to/category/dubbed-movies/page/%s?orderby=date'%(currPage)
        elif 'hlinksadult' in subUrl:
            hlinksurl = 'http://www.hindilinks4u.to/category/adult/page/%s?orderby=date'%(currPage)
        elif 'hlinksdocu' in subUrl:
            hlinksurl = 'http://www.hindilinks4u.to/category/documentaries/page/%s?orderby=date'%(currPage)
        elif 'hlinkssearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('HindiLinks4U')
                search_text = search_text.replace(' ', '+')
            hlinksurl = 'http://www.hindilinks4u.to/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_hlinks, hlinksurl)

    elif 'mersal' in subUrl:
            
        if 'mersal_Tamil' in subUrl:
            mersalurl = 'http://mersalaayitten.us/videos?c=1&o=mr&page=%s'%(currPage)
        elif 'mersal_Telugu' in subUrl:
            mersalurl = 'http://mersalaayitten.us/videos?c=3&o=mr&page=%s'%(currPage)
        elif 'mersal_Hindi' in subUrl:
            mersalurl = 'http://mersalaayitten.us/videos?c=2&o=mr&page=%s'%(currPage)
        elif 'mersal_Malayalam' in subUrl:
            mersalurl = 'http://mersalaayitten.us/videos?c=4&o=mr&page=%s'%(currPage)
        elif 'mersal_Dubbed' in subUrl:
            mersalurl = 'http://mersalaayitten.us/videos?c=6&o=mr&page=%s'%(currPage)
        elif 'mersal_Animation' in subUrl:
            mersalurl = 'http://mersalaayitten.us/videos?c=5&o=mr&page=%s'%(currPage)
        elif 'mersal_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Mersalaayitten')
                search_text = search_text.replace(' ', '+')
            mersalurl = 'http://mersalaayitten.us/search?search_type=videos&search_query=%s&page=%s'%(search_text,currPage)

        Dict_res = cache.cacheFunction(getMovList_mersal, mersalurl)

    elif 'mfish' in subUrl:

        if 'mfish_Tamil' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/watch-tamil/page/%s'%(currPage)
        elif 'mfish_Telugu' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/telugu/page/%s'%(currPage)
        elif 'mfish_Mal' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/watch-malayalam/page/%s'%(currPage)
        elif 'mfish_Hindi' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/all-video/page/%s'%(currPage)
        elif 'mfish_English' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/hollywood/page/%s'%(currPage)
        elif 'mfish_Dubbed' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/hindi-dubbed/page/%s'%(currPage)
        elif 'mfish_SDubbed' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/dubbed/page/%s'%(currPage)
        elif 'mfish_Punjabi' in subUrl:
            mfishurl = 'http://moviefisherhd.com/category/punjabi/page/%s'%(currPage)
        elif 'mfish_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('FirstTube')
                search_text = search_text.replace(' ', '+')
            mfishurl = 'http://moviefisherhd.com/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_mfish, mfishurl)

    elif 'tamiltv' in subUrl:

        tamiltvurl = 'http://www.tamiltvsite.com/browse-tamil-live-tv-videos-%s-date.html'%(currPage)
        Dict_res = cache.cacheFunction(getMovList_tamiltv, tamiltvurl)

    elif 'mrulz' in subUrl:

        if 'mrulz_Tamil' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/tamil-movie/page/%s/'%(currPage)
        elif 'mrulz_Telugu' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/telugu-movie/page/%s/'%(currPage)
        elif 'mrulz_Mal' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/malayalam-movie/page/%s/'%(currPage)
        elif 'mrulz_Kannada' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/kannada-movie/page/%s/'%(currPage)
        elif 'mrulz_h2016' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/bollywood-movie-2016/page/%s/'%(currPage)
        elif 'mrulz_h2015' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/bollywood-movie-2015/page/%s/'%(currPage)
        elif 'mrulz_h2014' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/bollywood-movie-2014/page/%s/'%(currPage)
        elif 'mrulz_e2016' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/hollywood-movie-2016/page/%s/'%(currPage)
        elif 'mrulz_e2015' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/hollywood-movie-2015/page/%s/'%(currPage)
        elif 'mrulz_e2014' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/hollywood-movie-2014/page/%s/'%(currPage)
        elif 'mrulz_hdubbed' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/hindi-dubbed-movie/page/%s/'%(currPage)
        elif 'mrulz_tdubbed' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/tamil-dubbed-movie-2/page/%s/'%(currPage)
        elif 'mrulz_tgdubbed' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/telugu-dubbed-movie-2/page/%s/'%(currPage)
        elif 'mrulz_Punjabi' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/punjabi-movie-2016/page/%s/'%(currPage)
        elif 'mrulz_Bengali' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/bengali-movie/page/%s/'%(currPage)
        elif 'mrulz_adult' in subUrl:
            mrulzurl = 'http://www.movierulz.ac/category/adult-movie/page/%s/'%(currPage)
        elif 'mrulz_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Movie Rulz')
                search_text = search_text.replace(' ', '+')
            mrulzurl = 'http://www.movierulz.ac/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_mrulz, mrulzurl)

    elif 'KitMovie' in subUrl:

        if 'KitMovie_Mal' in subUrl:
            kmovieurl = 'http://www.kitmovie.com/malayalam/categories/movie/page/%s/'%(currPage)
        elif 'KitMovie_MSongs' in subUrl:
            kmovieurl = 'http://www.kitmovie.com/malayalam/categories/songs/page/%s/'%(currPage)         
        elif 'KitMovie_Tamil' in subUrl:
            kmovieurl = 'http://www.kitmovie.com/tamil/categories/movie/page/%s/'%(currPage)
        elif 'KitMovie_TSongs' in subUrl:
            kmovieurl = 'http://www.kitmovie.com/tamil/categories/songs/page/%s/'%(currPage)       
        elif 'KitMovie_Hindi' in subUrl:
            kmovieurl = 'http://www.kitmovie.com/hindi/categories/movies/page/%s/'%(currPage)
        elif 'KitMovie_HSongs' in subUrl:
            kmovieurl = 'http://www.kitmovie.com/hindi/categories/songs/page/%s/'%(currPage)          
        elif 'KitMovie_tsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('FirstTube')
                search_text = search_text.replace(' ', '+')
            kmovieurl = 'http://www.kitmovie.com/tamil/page/%s/?s=%s'%(currPage,search_text)
        elif 'KitMovie_msearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('FirstTube')
                search_text = search_text.replace(' ', '+')
            kmovieurl = 'http://www.kitmovie.com/malayalam/page/%s/?s=%s'%(currPage,search_text)
        elif 'KitMovie_hsearch' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('FirstTube')
                search_text = search_text.replace(' ', '+')
            kmovieurl = 'http://www.kitmovie.com/hindi/page/%s/?s=%s'%(currPage,search_text)

        Dict_res = cache.cacheFunction(getMovList_KitMovie, kmovieurl)

    elif 'rmovies' in subUrl:
            
        if 'rmovies_Tamil' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/tamil/page/%s/'%(currPage)
        elif 'rmovies_Telugu' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/telugu/page/%s/'%(currPage)
        elif 'rmovies_Malayalam' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/malayalam/page/%s/'%(currPage)
        elif 'rmovies_Kannada' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/kannada-movies/page/%s/'%(currPage)
        elif 'rmovies_Hindi' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/bollywood-movies/page/%s/'%(currPage)
        elif 'rmovies_Dubbed' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/hindi-dubbed/page/%s/'%(currPage)
        elif 'rmovies_English' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/hollywood-movies/page/%s/'%(currPage)
        elif 'rmovies_Animated' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/animation/page/%s/'%(currPage)
        elif 'rmovies_Punjabi' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/punjabi-movies/page/%s/'%(currPage)
        elif 'rmovies_Urdu' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/pakistan/page/%s/'%(currPage)
        elif 'rmovies_Adult' in subUrl:
            rmoviesurl = 'http://redmovies.me/category/adult/page/%s/'%(currPage)
        elif 'rmovies_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('RedMovies')
                search_text = search_text.replace(' ', '+')
            rmoviesurl = 'http://redmovies.me/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_rmovies, rmoviesurl)

    elif 'moviefk' in subUrl:
            
        if 'moviefk_Tamil' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/tamil-movies/page/%s/'%(currPage)
        elif 'moviefk_Telugu' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/telugu-movies/page/%s/'%(currPage)
        elif 'moviefk_Marathi' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/marathi-movie/page/%s/'%(currPage)
        elif 'moviefk_Hindi' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/hindi-movies/page/%s/'%(currPage)
        elif 'moviefk_Dubbed' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/hindi-dubbed/page/%s/'%(currPage)
        elif 'moviefk_English' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/hollywood-movies/page/%s/'%(currPage)
        elif 'moviefk_WWE' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/wwe/page/%s/'%(currPage)
        elif 'moviefk_Punjabi' in subUrl:
            moviefkurl = 'http://www.moviefk.com/category/punjabi-movies/page/%s/'%(currPage)
        elif 'moviefk_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Full New Movie')
                search_text = search_text.replace(' ', '+')
            moviefkurl = 'http://www.moviefk.com/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_moviefk, moviefkurl)

    elif 'i4m' in subUrl:
            
        if 'i4m_Tamil' in subUrl:
            i4murl = 'http://www.india4movie.net/category/tamil-movie-list-2016-online-download//page/%s/'%(currPage)
        elif 'i4m_Telugu' in subUrl:
            i4murl = 'http://www.india4movie.net/category/telugu-movies/page/%s/'%(currPage)
        elif 'i4m_Marathi' in subUrl:
            i4murl = 'http://www.india4movie.net/category/marathi/page/%s/'%(currPage)
        elif 'i4m_Hindi' in subUrl:
            i4murl = 'http://www.india4movie.net/category/hindi-movie/page/%s/'%(currPage)
        elif 'i4m_Dubbed' in subUrl:
            i4murl = 'http://www.india4movie.net/category/dubbed-movie/page/%s/'%(currPage)
        elif 'i4m_English' in subUrl:
            i4murl = 'http://www.india4movie.net/category/hollywood-movie/page/%s/'%(currPage)
        elif 'i4m_Mal' in subUrl:
            i4murl = 'http://www.india4movie.net/category/malayalam-movie-list/page/%s/'%(currPage)
        elif 'i4m_Kan' in subUrl:
            i4murl = 'http://www.india4movie.net/category/kannada-new-movies-online/page/%s/'%(currPage)
        elif 'i4m_Punjabi' in subUrl:
            i4murl = 'http://www.india4movie.net/category/punjabi-movies-list/page/%s/'%(currPage)
        elif 'i4m_Bengali' in subUrl:
            i4murl = 'http://www.india4movie.net/category/bengali-new/page/%s/'%(currPage)
        elif 'i4m_Urdu' in subUrl:
            i4murl = 'http://www.india4movie.net/category/pakistani-movies/page/%s/'%(currPage)
        elif 'i4m_adult' in subUrl:
            i4murl = 'http://www.india4movie.net/category/adult-new-movie-xxx/page/%s/'%(currPage)
        elif 'i4m_search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('India 4 Movie')
                search_text = search_text.replace(' ', '+')
            i4murl = 'http://www.india4movie.net/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_i4m, i4murl)

    elif 'yd_' in subUrl:
   
        if 'main' in subUrl:
            ydurl = 'http://www.yodesi.net/page/%s/'%(currPage)
        elif 'star' in subUrl:
            ydurl = 'http://www.yodesi.net/category/star-plus/page/%s/'%(currPage)
        elif 'colors' in subUrl:
            ydurl = 'http://www.yodesi.net/category/colors/page/%s/'%(currPage)
        elif 'zee' in subUrl:
            ydurl = 'http://www.yodesi.net/category/zee-tv/page/%s/'%(currPage)
        elif 'sony' in subUrl:
            ydurl = 'http://www.yodesi.net/category/sony-tv/page/%s/'%(currPage)
        elif 'sab' in subUrl:
            ydurl = 'http://www.yodesi.net/category/sab-tv/page/%s/'%(currPage)
        elif 'lok' in subUrl:
            ydurl = 'http://www.yodesi.net/category/life-ok/page/%s/'%(currPage)
        elif 'jalsha' in subUrl:
            ydurl = 'http://www.yodesi.net/category/star-jalsha/page/%s/'%(currPage)
        elif 'and' in subUrl:
            ydurl = 'http://www.yodesi.net/category/tv/page/%s/'%(currPage)
        elif 'mtv' in subUrl:
            ydurl = 'http://www.yodesi.net/category/mtv-india/page/%s/'%(currPage)
        elif 'pravah' in subUrl:
            ydurl = 'http://www.yodesi.net/category/star-pravah/page/%s/'%(currPage)
        elif 'bind' in subUrl:
            ydurl = 'http://www.yodesi.net/category/bindass-tv/page/%s/'%(currPage)
        elif 'chv' in subUrl:
            ydurl = 'http://www.yodesi.net/category/channel-v/page/%s/'%(currPage)
        elif 'e24' in subUrl:
            ydurl = 'http://www.yodesi.net/category/e24/page/%s/'%(currPage)
        elif 'prom' in subUrl:
            ydurl = 'http://www.yodesi.net/category/promos-section/page/%s/'%(currPage)
        elif 'search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Yo Desi')
                search_text = search_text.replace(' ', '+')
            ydurl = 'http://www.yodesi.net/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_yd, ydurl)

    elif 'tts_' in subUrl:
   
        if 'main' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/page/%s/'%(currPage)
        elif 'sunss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/sun-tv-serials/page/%s/'%(currPage)
        elif 'sunsh' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/sun-tv-shows/page/%s/'%(currPage)
        elif 'vijayss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/vijay-tv-serials/page/%s/'%(currPage)
        elif 'vijaysh' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/vijay-tv-shows/page/%s/'%(currPage)
        elif 'zeess' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/zee-tamil-serials/page/%s/'%(currPage)
        elif 'zeesh' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/zee-tv-shows/page/%s/'%(currPage)
        elif 'rajss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/raj-tv-serials/page/%s/'%(currPage)
        elif 'rajsh' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/raj-tv-shows/page/%s/'%(currPage)
        elif 'polimerss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/polimer-tv-serials/page/%s/'%(currPage)
        elif 'captainss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/captain-tv-shows/page/%s/'%(currPage)
        elif 'jayass' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/jaya-tv-programs/page/%s/'%(currPage)
        elif 'kalaiss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/kalaignar-tv-shows/page/%s/'%(currPage)
        elif 'pyss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/puthuyugam/page/%s/'%(currPage)
        elif 'ptss' in subUrl:
            ttsurl = 'http://www.tamiltvshows.net/category/puthiya-thalaimurai-tv-shows/page/%s/'%(currPage)
        elif 'search' in subUrl:
            if currPage == 1:
                search_text = GetSearchQuery('Tamil TV Shows')
                search_text = search_text.replace(' ', '+')
            ttsurl = 'http://www.tamiltvshows.net/page/%s/?s=%s'%(currPage,search_text)
            
        Dict_res = cache.cacheFunction(getMovList_tts, ttsurl)

    keylist = Dict_res.keys()
    mov_menu(keylist)        
    dlg.close()

elif mode == 'olangal':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'olangalMovies'}, {'title': 'Recent Movies'}, img=olangal_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'olangalsearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=olangal_img, fanart=fan_img)

elif mode == 'abcmalayalam':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ABCMalayalam-Mal'}, {'title': 'Malayalam Movies'}, img=abcm_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ABCMalayalam-shortFilm'}, {'title': 'Malayalam Short Films'}, img=abcm_img, fanart=fan_img)

elif mode == 'rajTamil':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamilRecent'}, {'title': 'Tamil Recent Movies'}, img=rajt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamildubbed'}, {'title': 'Tamil Dubbed Movies'}, img=rajt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamilcomedy'}, {'title': 'Tamil Movie Comedy Scenes'}, img=rajt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamilsongs'}, {'title': 'Tamil Movie Songs'}, img=rajt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamilTVshowsSunTV'}, {'title': 'TV Shows - Sun TV'}, img=rajt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamilTVshowsVijayTV'}, {'title': 'TV Shows - Vijay TV'}, img=rajt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rajtamilsearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=rajt_img, fanart=fan_img)

elif mode == 'tamilgun':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamilgunnew'}, {'title': 'Tamil New Movies'}, img=tgun_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamilgunhd'}, {'title': 'Tamil HD Movies'}, img=tgun_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamilgundubbed'}, {'title': 'Tamil Dubbed Movies'}, img=tgun_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamilguncomedy'}, {'title': 'Tamil Movie Comedy Scenes'}, img=tgun_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamilguntrailer'}, {'title': 'Tamil Movie Trailers'}, img=tgun_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamilgunsearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=tgun_img, fanart=fan_img)

elif mode == 'tyogi':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_new'}, {'title': 'Tamil New Movies'}, img=tyogi_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_hd'}, {'title': 'Tamil HD Movies'}, img=tyogi_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_dvd'}, {'title': 'Tamil DVD Movies'}, img=tyogi_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_dubbed'}, {'title': 'Tamil Dubbed Movies'}, img=tyogi_img, fanart=fan_img)
    #_DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_songs'}, {'title': 'Tamil Movie Video Songs'}, img=tyogi_img, fanart=fan_img)
    #_DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_trailer'}, {'title': 'Tamil Movie Trailers'}, img=tyogi_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tyogi_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=tyogi_img, fanart=fan_img)

elif mode == 'runtamil':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'runtamilnew'}, {'title': 'Tamil New Movies'}, img=runt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'runtamilhd'}, {'title': 'Tamil HD Movies'}, img=runt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'runtamildvd'}, {'title': 'Tamil DVD Movies'}, img=runt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'runtamilold'}, {'title': 'Tamil Classic Movies'}, img=runt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'runtamildubbed'}, {'title': 'Tamil Dubbed Movies'}, img=runt_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'runtamilsearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=runt_img, fanart=fan_img)

elif mode == 'ttwist':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwistnew'}, {'title': 'Tamil New Movies'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwisthd'}, {'title': 'Tamil HD Movies'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwistdubbed'}, {'title': 'Tamil Dubbed Movies'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwisttrailer'}, {'title': 'Tamil Movie Trailers'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwistmal'}, {'title': 'Malayalam Movies'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwisttel'}, {'title': 'Telugu Movies'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwisthin'}, {'title': 'Hindi Movies'}, img=ttwist_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwistadult'}, {'title': 'Adult Movies'}, img=ttwist_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'ttwistsearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=ttwist_img, fanart=fan_img)

elif mode == 'flinks':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkstamil'}, {'title': 'Tamil Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksmalayalam'}, {'title': 'Malayalam Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkstelugu'}, {'title': 'Telugu Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkshindi'}, {'title': 'Hindi Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkskannada'}, {'title': 'Kannada Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksani'}, {'title': 'Animation Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksholly'}, {'title': 'English Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksbio'}, {'title': 'Biography Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksdocu'}, {'title': 'Documentary Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksben'}, {'title': 'Bengali Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksbhoj'}, {'title': 'Bhojpuri Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksguj'}, {'title': 'Gujarati Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksmar'}, {'title': 'Marathi Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksnep'}, {'title': 'Nepali Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksori'}, {'title': 'Oriya Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkspun'}, {'title': 'Punjabi Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksraj'}, {'title': 'Rajasthani Movies'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksurdu'}, {'title': 'Urdu Movies'}, img=flinks_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinksadult'}, {'title': 'Adult Movies'}, img=flinks_img, fanart=fan_img)
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkshindisc'}, {'title': 'Hindi Softcore'}, img=flinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'flinkssearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=flinks_img, fanart=fan_img)

elif mode == 'hlinks':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'hlinkshindi'}, {'title': 'Hindi Movies'}, img=hlinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'hlinksdub'}, {'title': 'Dubbed Movies'}, img=hlinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'hlinksdocu'}, {'title': 'Documentary Movies'}, img=hlinks_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'hlinksadult'}, {'title': 'Adult Movies'}, img=hlinks_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'hlinkssearch'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=hlinks_img, fanart=fan_img)

elif mode == 'thiruttuvcd':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_tamilMovs'}, {'title': 'Tamil Movies'}, img=tvcd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_MalayalamMovs'}, {'title': 'Malayalam Movies'}, img=tvcd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_teluguMovs'}, {'title': 'Telugu Movies'}, img=tvcd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_hindiMovs'}, {'title': 'Hindi Movies'}, img=tvcd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_tamiltv'}, {'title': 'Tamil TV Shows'}, img=tvcd_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_adult'}, {'title': 'Adult Movies'}, img=tvcd_img, fanart=fan_img)
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_masala'}, {'title': 'Thiruttu Masala'}, img=tvcd_img, fanart=fan_img)
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_msearch'}, {'title': '[COLOR yellow]** Search Masala **[/COLOR]'}, img=tvcd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'thiruttuvcd_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=tvcd_img, fanart=fan_img)
 
elif mode == 'tvcds':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tvcds_tamil'}, {'title': 'Tamil Movies'}, img=tvcds_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tvcds_telugu'}, {'title': 'Telugu Movies'}, img=tvcds_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tvcds_hindi'}, {'title': 'Hindi Movies'}, img=tvcds_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tvcds_english'}, {'title': 'English Movies'}, img=tvcds_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tvcds_adult'}, {'title': 'Adult Movies'}, img=tvcds_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tvcds_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=tvcds_img, fanart=fan_img)
    
elif mode == 'mersal':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_Tamil'}, {'title': 'Tamil Movies'}, img=mersal_img, fanart=fan_img)        
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_Telugu'}, {'title': 'Telugu Movies'}, img=mersal_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_Hindi'}, {'title': 'Hindi Movies'}, img=mersal_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_Malayalam'}, {'title': 'Malayalam Movies'}, img=mersal_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_Dubbed'}, {'title': 'Dubbed Movies'}, img=mersal_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_Animation'}, {'title': 'Animation Movies'}, img=mersal_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mersal_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=mersal_img, fanart=fan_img)

elif mode == 'mfish':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_Tamil'}, {'title': 'Tamil Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_Telugu'}, {'title': 'Telugu Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_Mal'}, {'title': 'Malayalam Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_Hindi'}, {'title': 'Hindi Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_English'}, {'title': 'English Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_Dubbed'}, {'title': 'Hindi Dubbed Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_SDubbed'}, {'title': 'Hindi Dubbed South Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_Punjabi'}, {'title': 'Punjabi Movies'}, img=mfish_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mfish_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=mfish_img, fanart=fan_img)

elif mode == 'mrulz':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_Tamil'}, {'title': 'Tamil Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_Telugu'}, {'title': 'Telugu Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_Mal'}, {'title': 'Malayalam Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_Kannada'}, {'title': 'Kannada Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_h2016'}, {'title': 'Hindi 2016 Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_h2015'}, {'title': 'Hindi 2015 Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_h2014'}, {'title': 'Hindi 2014 Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_e2016'}, {'title': 'English 2016 Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_e2015'}, {'title': 'English 2015 Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_e2014'}, {'title': 'English 2014 Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_tdubbed'}, {'title': 'Tamil Dubbed Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_tgdubbed'}, {'title': 'Telugu Dubbed Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_hdubbed'}, {'title': 'Hindi Dubbed Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_Bengali'}, {'title': 'Bengali Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_Punjabi'}, {'title': 'Punjabi Movies'}, img=mrulz_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_adult'}, {'title': 'Adult Movies'}, img=mrulz_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'mrulz_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=mrulz_img, fanart=fan_img)
    
elif mode == 'rmovies':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Tamil'}, {'title': 'Tamil Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Telugu'}, {'title': 'Telugu Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Malayalam'}, {'title': 'Malayalam Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Hindi'}, {'title': 'Hindi Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_English'}, {'title': 'English Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Animated'}, {'title': 'Animation Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Dubbed'}, {'title': 'Hindi Dubbed Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Kannada'}, {'title': 'Kannada Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Punjabi'}, {'title': 'Punjabi Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Urdu'}, {'title': 'Urdu Movies'}, img=rmovies_img, fanart=fan_img)
    # if SETTINGS_ADULT == 'true':
        # _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_Adult'}, {'title': 'Adult Movies'}, img=rmovies_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'rmovies_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=rmovies_img, fanart=fan_img)

elif mode == 'moviefk':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_Tamil'}, {'title': 'Tamil Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_Telugu'}, {'title': 'Telugu Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_Hindi'}, {'title': 'Hindi Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_English'}, {'title': 'English Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_Dubbed'}, {'title': 'Hindi Dubbed Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_Punjabi'}, {'title': 'Punjabi Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_Marathi'}, {'title': 'Marathi Movies'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_WWE'}, {'title': 'WWE events'}, img=moviefk_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'moviefk_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=moviefk_img, fanart=fan_img)

elif mode == 'i4m':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Tamil'}, {'title': 'Tamil Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Telugu'}, {'title': 'Telugu Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Mal'}, {'title': 'Malayalam Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Kan'}, {'title': 'Kannada Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Hindi'}, {'title': 'Hindi Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_English'}, {'title': 'English Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Dubbed'}, {'title': 'Hindi Dubbed Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Punjabi'}, {'title': 'Punjabi Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Marathi'}, {'title': 'Marathi Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Bengali'}, {'title': 'Bengali Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_Urdu'}, {'title': 'Urdu Movies'}, img=i4m_img, fanart=fan_img)
    if SETTINGS_ADULT == 'true':
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_adult'}, {'title': 'Adult Movies'}, img=i4m_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'i4m_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=i4m_img, fanart=fan_img)

elif mode == 'yodesi':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_main'}, {'title': 'Recently Added'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_star'}, {'title': 'Star Plus'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_colors'}, {'title': 'Colors'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_zee'}, {'title': 'Zee TV'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_sony'}, {'title': 'Sony TV'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_sab'}, {'title': 'SAB TV'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_lok'}, {'title': 'Life OK'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_jalsha'}, {'title': 'Star Jalsha'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_and'}, {'title': '& TV'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_pravah'}, {'title': 'Star Pravah'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_mtv'}, {'title': 'MTV'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_bind'}, {'title': 'Bindass'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_chv'}, {'title': 'Channel V'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_e24'}, {'title': 'E 24'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_prom'}, {'title': 'Promos'}, img=yd_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yd_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=yd_img, fanart=fan_img)

elif mode == 'ttshows':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_main'}, {'title': 'Recently Added'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_sunss'}, {'title': 'Sun TV Series'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_sunsh'}, {'title': 'Sun TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_vijayss'}, {'title': 'Vijay TV Series'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_vijaysh'}, {'title': 'Vijay TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_zeess'}, {'title': 'Zee Tamil TV Series'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_zeesh'}, {'title': 'Zee Tamil TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_rajss'}, {'title': 'Raj TV Series'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_rajsh'}, {'title': 'Raj TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_polimerss'}, {'title': 'Polimer TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_captainss'}, {'title': 'Captain TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_jayass'}, {'title': 'Jaya TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_kalaiss'}, {'title': 'Kalaignar TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_pyss'}, {'title': 'Puthuyugam TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_ptss'}, {'title': 'Puthiya Thalaimurai TV Shows'}, img=tts_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tts_search'}, {'title': '[COLOR yellow]** Search **[/COLOR]'}, img=tts_img, fanart=fan_img)
    
elif mode == 'KitMovie':
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_Tamil'}, {'title': 'Tamil Movies'}, img=kmovie_img, fanart=fan_img) 
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_TSongs'}, {'title': 'Tamil Music Videos'}, img=kmovie_img, fanart=fan_img)       
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_Mal'}, {'title': 'Malayalam Movies'}, img=kmovie_img, fanart=fan_img)    
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_MSongs'}, {'title': 'Malayalam Music Videos'}, img=kmovie_img, fanart=fan_img) 
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_Hindi'}, {'title': 'Hindi Movies'}, img=kmovie_img, fanart=fan_img)   
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_HSongs'}, {'title': 'Hindi Music Videos'}, img=kmovie_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_tsearch'}, {'title': '[COLOR yellow]** Search Tamil **[/COLOR]'}, img=kmovie_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_msearch'}, {'title': '[COLOR yellow]** Search Malayalam **[/COLOR]'}, img=kmovie_img, fanart=fan_img)
    _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'KitMovie_hsearch'}, {'title': '[COLOR yellow]** Search Hindi **[/COLOR]'}, img=kmovie_img, fanart=fan_img)
    
elif mode == 'main':
    if SETTINGS_TamilGun == 'true':
        _DD.add_directory({'mode': 'tamilgun'}, {'title': 'Tamil Gun : [COLOR yellow]Tamil[/COLOR]'}, img=tgun_img, fanart=fan_img)
    if SETTINGS_RajTamil == 'true':    
        _DD.add_directory({'mode': 'rajTamil'}, {'title': 'Raj Tamil : [COLOR yellow]Tamil[/COLOR]'}, img=rajt_img, fanart=fan_img)
    if SETTINGS_TamilYogi == 'true':   
        _DD.add_directory({'mode': 'tyogi'}, {'title': 'Tamil Yogi : [COLOR yellow]Tamil[/COLOR]'}, img=tyogi_img, fanart=fan_img)
    if SETTINGS_RunTamil == 'true':    
        _DD.add_directory({'mode': 'runtamil'}, {'title': 'Run Tamil : [COLOR yellow]Tamil[/COLOR]'}, img=runt_img, fanart=fan_img)
    if SETTINGS_APKLand == 'true':    
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'tamiltv'}, {'title': 'APKLand TV : [COLOR yellow]Tamil Live TV[/COLOR]'}, img=ttvs_img, fanart=fan_img)
    if SETTINGS_TamilTVS == 'true':
        _DD.add_directory({'mode': 'ttshows'}, {'title': 'Tamil TV Shows : [COLOR yellow]Tamil Catchup TV[/COLOR]'}, img=tts_img, fanart=fan_img)
    if SETTINGS_ABCMal == 'true':    
        _DD.add_directory({'mode': 'abcmalayalam'}, {'title': 'ABC Malayalam : [COLOR yellow]Malayalam[/COLOR]'}, img=abcm_img, fanart=fan_img)
    if SETTINGS_Olangal == 'true':         
        _DD.add_directory({'mode': 'olangal'}, {'title':'Olangal : [COLOR yellow]Malayalam[/COLOR]'}, img=olangal_img, fanart=fan_img)
    if SETTINGS_LiveMal == 'true':         
        _DD.add_directory({'mode': 'GetMovies', 'subUrl': 'lmtv'}, {'title': 'Live Malayalam : [COLOR yellow]Malayalam Live TV[/COLOR]'}, img=lmtv_img, fanart=fan_img)
    if SETTINGS_HLinks == 'true':         
        _DD.add_directory({'mode': 'hlinks'}, {'title': 'Hindi Links 4U : [COLOR yellow]Hindi[/COLOR]'}, img=hlinks_img, fanart=fan_img)
        #_DD.add_directory({'mode': 'GetMovies', 'subUrl': 'yamgo'}, {'title': 'Yamgo TV : [COLOR yellow]Hindi Live TV[/COLOR]'}, img=yamgo_img, fanart=fan_img)
    if SETTINGS_YoDesi == 'true':         
        _DD.add_directory({'mode': 'yodesi'}, {'title': 'Yo Desi : [COLOR yellow]Hindi Catchup TV[/COLOR]'}, img=yd_img, fanart=fan_img)
    if SETTINGS_TVCD == 'true':         
        _DD.add_directory({'mode': 'thiruttuvcd'}, {'title': 'Thiruttu VCD : [COLOR magenta]Various[/COLOR]'}, img=tvcd_img, fanart=fan_img)
    if SETTINGS_KitMovie == 'true':         
        _DD.add_directory({'mode': 'KitMovie'}, {'title': 'Kit Movie : [COLOR magenta]Various[/COLOR]'}, img=kmovie_img, fanart=fan_img)
    if SETTINGS_TTwists == 'true':        
       _DD.add_directory({'mode': 'ttwist'}, {'title': 'Tamil Twists : [COLOR magenta]Various[/COLOR]'}, img=ttwist_img, fanart=fan_img)
    if SETTINGS_MRulz == 'true':        
       _DD.add_directory({'mode': 'mrulz'}, {'title': 'Movie Rulz : [COLOR magenta]Various[/COLOR]'}, img=mrulz_img, fanart=fan_img)
    if SETTINGS_FLinks == 'true':
        _DD.add_directory({'mode': 'flinks'}, {'title': 'Film Links 4U : [COLOR magenta]Various[/COLOR]'}, img=flinks_img, fanart=fan_img)
    if SETTINGS_MovieFK == 'true':         
        _DD.add_directory({'mode': 'moviefk'}, {'title': 'Movie FK : [COLOR magenta]Various[/COLOR]'}, img=moviefk_img, fanart=fan_img)
    if SETTINGS_I4M == 'true':         
        _DD.add_directory({'mode': 'i4m'}, {'title': 'India 4 Movie : [COLOR magenta]Various[/COLOR]'}, img=i4m_img, fanart=fan_img)
    if SETTINGS_MFish == 'true':         
        _DD.add_directory({'mode': 'mfish'}, {'title': 'Movie Fisher : [COLOR magenta]Various[/COLOR]'}, img=mfish_img, fanart=fan_img)
    if SETTINGS_RedM == 'true':         
        _DD.add_directory({'mode': 'rmovies'}, {'title': 'Red Movies : [COLOR magenta]Various[/COLOR]'}, img=rmovies_img, fanart=fan_img)
    if SETTINGS_Mersal == 'true': 
        _DD.add_directory({'mode': 'mersal'}, {'title': 'Mersalaayitten : [COLOR magenta]Various[/COLOR]'}, img=mersal_img, fanart=fan_img)
    if SETTINGS_TVCDs == 'true':        
        _DD.add_directory({'mode': 'tvcds'}, {'title': 'Thiruttu VCDs : [COLOR magenta]Various[/COLOR]'}, img=tvcds_img, fanart=fan_img)


if not play:
    _DD.end_of_directory()
