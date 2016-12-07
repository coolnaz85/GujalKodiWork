'''
tamiltv deccandelight plugin
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
import urllib, re, requests, json

class tamiltv(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.tamiltvsite.com/'
        self.rbu = 'http://radio.tamiltvsite.com/'
        self.icon = self.ipath + 'apkland.png'
        self.list = {'01Entertainment Channels': self.bu + 'browse-tamil-tv-videos-1-title.html',
                     '02Music Channels': self.bu + 'browse-tamil-music-tv-videos-1-title.html',
                     '03News Channels': self.bu + 'browse-tamil-news-videos-1-title.html',
                     '04HD Channels': self.bu + 'browse-tamil-hd-videos-1-title.html',
                     '05Devotional Channels': self.bu + 'browse-tamil-devotional-tv-videos-1-title.html',
                     '06Tamil Radio': self.rbu + '?c=all',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu + 'search.php?keywords='}
  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        movies = []
        if url[-9:] == 'keywords=':
            search_text = self.get_SearchQuery('APKLand TV')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        
        if 'radio' in url:
            items = json.loads(html)
            for item in items:
                title = item['name']
                url = item['streams']['Default Quality']['mp3']
                if 'radionomy.com' in url:
                    url += '.m3u'
                try:
                    thumb = self.rbu + item['logo']
                except:
                    thumb = self.icon
                movies.append((title, thumb, url))
        else:
            mlink = SoupStrainer('ul', {'id':'pm-grid'})
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            plink = SoupStrainer('div', {'class':'pagination pagination-centered'})
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)
            items = mdiv.findAll('div', {'class':'pm-li-video'})
            for item in items:
                title = item.h3.text.encode('utf8')
                url = item.find('a')['href']
                try:
                    thumb = item.find('img')['src']
                except:
                    thumb = self.icon
                movies.append((title, thumb, url))

            pages = Paginator.findAll('li', {'class':''})
            if '&raquo;' in str(pages):
                currpg = Paginator.find('li', {'class':'active'}).text            
                purl = pages[len(pages)-1].find('a')['href']
                lastpg = pages[len(pages)-2].text
                title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
                movies.append((title, self.nicon, purl))
        
        return (movies,9)
      
    def get_video(self,url):

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':'Playerholder'})
        soup = BeautifulSoup(html, parseOnlyThese=mlink)
        stream_url = None

        tlink = soup.iframe.get('src')
        link = requests.get(tlink, headers=self.hdr).text
        strdata = re.findall('var act_data = ({.*?});', link)[0]
        act_data = json.loads(strdata)
        act_url = act_data["url"]
        if '>>>>' in act_url:
            act_url = act_url.split('>>>>')[0]
        act_url = '%schannels/channel.php?%s'%(self.bu, act_url.split('?')[1])
        link = requests.get(act_url, headers=self.hdr).text
        strdata = re.findall('act_data = ({.*?});', link)[0]
        act_data = json.loads(strdata)
        tlink = act_data["url"]
        
        if 'embed.' in tlink:
            stream_url = tlink.split('embed')[0] + 'index.m3u8'
        
        elif 'wmsAuthSign' in tlink:
            new_token = re.findall('new_token = "(.*?)"', link)[0]
            stream_url = tlink.split('?')[0] + '?wmsAuthSign=' + new_token
                
        elif ('dacast.' in tlink) or ('streamingasaservice.' in tlink):
            surl = tlink.split('.com')[1]
            headers = self.hdr
            headers['Referer'] = 'http://iframe.dacast.com/'
            link = requests.get('http://json.dacast.com' + surl, headers=headers).text
            act_data = json.loads(link)
            act_url = act_data["hls"]
            link = requests.get('https://services.dacast.com/token/i%s?'%surl, headers=headers, verify=False).text
            act_data = json.loads(link)
            new_token = act_data["token"]
            stream_url = act_url + new_token
                        
        elif any([x in tlink for x in ['youtube', '.m3u8', 'rtmp:']]):
            stream_url = tlink

        elif 'chennaistream.net' in tlink:
            link = requests.get(tlink, headers=self.hdr).text
            tcurl = re.findall("netConnectionUrl: '(.*?)'", link)[0]
            stream_url = '%s playpath=mp4:%slive live=1 timeout=15'%(tcurl, tcurl.split('/')[3])

            
        return stream_url
