'''
mersalaayitten deccandelight plugin
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

class mersal(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://mersalaayitten.us/videos?c='
        self.icon = self.ipath + 'mersal.png'
        self.list = {'01Tamil Movies': self.bu + '1&o=mr',
                     '02Telugu Movies': self.bu + '3&o=mr',
                     '03Hindi Movies': self.bu + '2&o=mr',
                     '04Malayalam Movies': self.bu + '4&o=mr',
                     '05Dubbed Movies': self.bu + '6&o=mr',
                     '06Animation Movies': self.bu + '5&o=mr',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + 'search?search_type=videos&search_query='}
   
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        movies = []
        if '%' in url:
            url = urllib.unquote(url)
        if url[-6:] == 'query=':
            search_text = self.get_SearchQuery('Mersalaayitten')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'col-md-9 col-sm-8'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer("ul", {"class":"pagination pagination-lg"})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':'col-sm-6 col-md-4 col-lg-4'})
        for item in items:
            title = item.find('span').text.encode('utf8')
            url = item.find('a')['href']
            url = self.bu[:-9] + 'embed/' + url.split('/')[2]
            try:
                thumb = item.find('img')['data-original']
            except:
                thumb = item.find('img')['src']
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextpg = Paginator.find('a', {'class':'prevnext'})
            purl = nextpg.get('href')
            purl = urllib.quote_plus(purl)
            currpg = Paginator.find('li', {'class':'active'}).text
            pages = Paginator.findAll('li', {'class':'hidden-xs'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,9)
      
    def get_video(self,url):

        url = self.bu[:-9] + 'embed/' + url.split('/')[4]
        headers = self.hdr
        r = requests.get(url, headers=headers)
        link = r.text
        cookies = r.cookies
        avs = cookies['AVS']
        xmlurl = re.findall('config=(.*?)"', link)[0]
        headers['Referer'] = '%smedia/nuevo/player.swf?config=%s'%(self.bu[:-9],xmlurl)

        r = requests.get(xmlurl, headers=headers, cookies=cookies)
        link = r.text

        soup = BeautifulSoup(link)

        try:
            stream_url = soup.file.text + '|Cookie=AVS=%s'%avs
            try:
                srtfile = soup.captions.text
            except:
                srtfile = None
        except:
            pass
            
        return (stream_url,srtfile)