'''
livemalayalamtv deccandelight plugin
Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
from main import Scraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, re, requests
import HTMLParser

class aindia(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://abroadindia.com/'
        self.icon = self.ipath + 'aindia.png'
        self.list = {'01Tamil Channels': self.bu + 'tamiltv',
                     '02Telugu Channels': self.bu + 'telugutv',
                     '03Malayalam Channels': self.bu + 'malayalamtv',
                     '04Kannada Channels': self.bu + 'kannadatv',
                     '05Hindi Channels': self.bu + 'hinditv',
                     '06English Channels': self.bu + 'englishtv'}
  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('ul', {'id':'nav'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        cid = re.findall('cid="(.*?)"',html)[0]
        items = mdiv.findAll('td')
        for item in items:
            if 'href' in str(item):
                title = h.unescape(item.text)
                chid = item.find('a')['id']
                url = self.bu + 'ZZZZ%sZZZZ%s'%(cid,chid)
                try:
                    thumb = item.find('img')['src']
                except:
                    thumb = self.icon
                movies.append((title, thumb, url))

        movies.sort()
        
        return (movies,9)
      
    def get_video(self,iurl):

        cid = iurl.split('ZZZZ')[1]
        pid = iurl.split('ZZZZ')[2]
        values = {'tid': '',
                  'cid': cid,
                  'page': pid}
        purl = self.bu + 'm_load.php'
        headers = self.hdr
        headers['Referer'] = self.bu
        url = requests.post(purl, data=values, headers=headers).text
        
        html = requests.get(url, headers=headers).text
        sid = re.findall('sid="(.*?)"',html)[0]
        fspid = re.findall('sid="(.*?)"',html)[0]
        url = self.bu + 'm_loadplayer.php?channel=&tid=&cid=&sid=%s&fspid=%s'%(sid,fspid)
        html = requests.get(url, headers=headers).text
        sid = re.findall('sid="(.*?)"',html)[0]
        url = self.bu + 'm_loadframe1.php?channel=&tid=&cid=&sid=%s&fspid='%sid
        html = requests.get(url, headers=headers).text
        pid = re.findall('pid="(.*?)"',html)[0]
        headers1 = headers
        headers1['X-Requested-With'] = 'XMLHttpRequest'
        url = self.bu + 'm_loadfram.php?tid=&cid=&pid=%s&fspid=&sid=%s'%(pid,sid)
        html = requests.get(url, headers=headers1).text
        url = re.findall('<iframe.*?src="(.*?)"',html)[0]
        if 'player_amain' in url:
            html = requests.get(url, headers=headers).text
            fpid = re.findall('fpid="(.*?)"',html)[0]
            url = self.bu + 'm_player_echo_hls.php'
            values = {'fpid': fpid}
            stream_url = requests.post(url, data=values, headers=headers).text
        
        elif 'player_yup' in url:
            html = requests.get(url, headers=headers).text
            url = re.findall('src=([^\s]*)',html)[0]
            html = requests.get(url, headers=headers).text
            stream_url = re.findall("file:\s?'(.*?m3u8.*?)'",html)[0]

        elif 'player_iframe' in url:
            html = requests.get(url, headers=headers).text
            try:
                url = re.findall('iframe.*?src=([^\s]*)',html)[0]
            except:
                url = re.findall('(http.*?)</div',html)[0]
            url = url.replace('"','')
            if 'youtube' in url:
                stream_url = url
            elif 'abroadindia' in url:
                html = requests.get(url, headers=headers).text
                if 'video=' in html:
                    stream_url = re.findall('video="(.*?)"',html)[0]
                elif 'iframe' in html:
                    stream_url = re.findall('iframe.*?src="(.*?)"',html)[0]
            elif 'embed.' in url:
                stream_url = url.split('embed')[0] + 'index.m3u8'
            elif 'holygod' in url:
                html = requests.get(url, headers=headers).text
                url = re.findall("script src='(.*?)'",html)[0]
                html = requests.get(url, headers=headers).text
                stream_url = re.findall('ipadUrl:"(.*?)"',html)[0]
            elif 'uthamiyae.' in url or 'filmon.' in url or 'livestream.' in url:
                stream_url = None
            else:
                html = requests.get(url, headers=headers).text
                try:
                    stream_url = re.findall('"(.*?m3u8.*?)"',html)[0]
                except:
                    stream_url = re.findall("file:\s?'(.*?)'",html)[0]
            
        else:
            stream_url = None
            
        return stream_url
