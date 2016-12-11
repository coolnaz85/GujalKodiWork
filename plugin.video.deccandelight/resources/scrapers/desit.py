'''
desitashan deccandelight plugin
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

class desit(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.desitashan.me/'
        self.icon = self.ipath + 'desit.png'
        self.list = {'01Indian': self.bu,
                     '02Pakistani': self.bu + 'pakistan-tv/'}
            
    def get_menu(self):
        return (self.list,4,self.icon)

    def get_top(self,url):
        """
        Get the list of channels.
        :return: list
        """
        channels = []
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'nav fusion-mobile-tab-nav'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        for item in items:
            title = item.text
            tref = item.a.get('href')[1:]
            iurl = '%sZZZZ%s'%(url,tref)
            try:
                icon = item.find('img')['src']
                if icon.startswith('/'):
                    icon = self.bu[:-1] + icon
                else:
                    icon = self.bu + icon
            except:
                icon = self.icon
            
            channels.append((title,icon,iurl))

        return (channels,5)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        url = iurl.split('ZZZZ')[0]
        channel = iurl.split('ZZZZ')[1]
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':channel})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':'fusion-column-wrapper'})
        for item in items:
            title = item.text
            url = item.a.get('href')
            if url.startswith('/'):
                url = self.bu[:-1] + url
            else:
                url = self.bu + url
            try:
                icon = item.find('img')['src']
                if icon.startswith('/'):
                    icon = self.bu[:-1] + icon
                else:
                    icon = self.bu + icon
            except:
                icon = self.icon
            
            shows.append((title,icon,url))
        
        return (shows,7)
        
    def get_items(self,iurl):
        episodes = []
        html = requests.get(iurl).text
        mlink = SoupStrainer('div', {'id':'showList'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':'fusion-column-wrapper'})
        for item in items:
            title = item.h4.a.text
            if 'written' not in title.lower():
                url = item.a.get('href')
                if url.startswith('/'):
                    url = self.bu[:-1] + url
                else:
                    url = self.bu + url
                try:
                    icon = item.find('img')['src']
                    if icon.startswith('/'):
                        icon = self.bu[:-1] + icon
                    else:
                        icon = self.bu + icon
                except:
                    icon = self.icon           
                episodes.append((title,icon,url))
        plink = SoupStrainer('a', {'class':'pagination-next'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        if 'Next' in str(Paginator):
            ep_link = Paginator.a.get('href')
            if 'category' in ep_link:
                url = self.bu[:-1] + ep_link
            else:
                url = iurl + ep_link
            title = 'Next Page: ' + url.split('page/')[1][:-1]
            episodes.append((title, self.nicon, url))    
        return (episodes,8) 

    def get_videos(self,iurl):
        videos = []
        html = requests.get(iurl).text
        mlink = SoupStrainer('p', {'class':'vidLinksContent'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        items = videoclass.findAll('a')
        for item in items:
            vid_link = item['href']
            if '/coming/' in vid_link:
                url = 'http://www.tashanplayer.com/upcoming.mp4'
                videos.append(('DT Upcoming',url))
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
                self.resolve_media(vid_url,videos)
            else:
                self.resolve_media(vid_link,videos)

        mlink = SoupStrainer('div', {'class':'post-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        items = videoclass.findAll('iframe')
        for item in items:
            vid_link = item['src']
            if '/coming/' in vid_link:
                url = 'http://www.tashanplayer.com/upcoming.mp4'
                videos.append(('DT Upcoming',url))
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
                self.resolve_media(vid_url,videos)
            else:
                self.resolve_media(vid_link,videos)
            
        return videos
