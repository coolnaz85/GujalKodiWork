'''
AndhraWatch DeccanDelight plugin
Copyright (C) 2017 Gujal

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

class awatch(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.andhrawatch.com/'
        self.icon = self.ipath + 'awatch.png'
        self.list = {'01Movies': self.bu + 'telugu-movies/',
                     '02Trailers': self.bu + 'movie-trailers/',
                     '03Short Films': self.bu + 'short-films/'}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'cat-box-content'})
        itemclass = BeautifulSoup(html, parseOnlyThese=mlink)
        items = itemclass.findAll('div', {'class':'recent-item'})

        for item in items:
            title = h.unescape(item.h3.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
 
        plink = SoupStrainer('div', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink) 
        nextdivs = Paginator.findAll('a', {'class':None})
        for nexts in nextdivs:
            if nexts.text == '&raquo;':
                pgtxt = Paginator.find('span', {'class':'pages'}).text
                purl = nexts.get('href')
                title = 'Next Page.. (Currently in %s)' % pgtxt
                movies.append((title, self.nicon, purl))
        
        return (movies,9)

    def get_video(self,url):
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('iframe')
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            vidurl = videoclass.find('iframe')['src'].split('?')[0]
        except:
            pass
      
        return vidurl
